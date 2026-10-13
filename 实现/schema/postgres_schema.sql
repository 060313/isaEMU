-- ============================================================================
-- ISA 模拟系统 —— PostgreSQL 形态的库结构（11 张表 / 83 列 / 13 个外键 / 9 个索引）
--
-- 设计依据：《软件详细设计文档》7.3（T-01 ~ T-11、FK-01 ~ FK-13、IX-01 ~ IX-09）
-- 说明：与 sqlite_schema.sql 同源（SA-09）；7 处 DDL 差异见 7.2.2。本文件是云端形态。
--       表按外键依赖顺序排列（PG 要求被引用表先存在）。
-- ============================================================================

-- 版本表：启动序列统一检查（7.4.6）
CREATE TABLE schema_version (
  version INTEGER NOT NULL
);

-- T-01 users —— 用户身份、角色、配额、状态（9 列）
CREATE TABLE users (
  uid         BIGINT       PRIMARY KEY,               -- 由 IIdGen 生成（G-2），不用自增
  username    VARCHAR(64)  NOT NULL UNIQUE,           -- IX-01
  role        SMALLINT     NOT NULL DEFAULT 0,        -- E-18：0 = User, 1 = Admin
  q_sessions  INTEGER      NOT NULL DEFAULT 64,
  q_requests  INTEGER      NOT NULL DEFAULT 600,
  q_instr     BIGINT       NOT NULL DEFAULT 10000000, -- NFR-Q5
  q_bytes     BIGINT       NOT NULL DEFAULT 67108864, -- 64 MiB
  status      SMALLINT     NOT NULL DEFAULT 0,        -- E-19：0 = Active, 1 = Disabled
  created_at  TIMESTAMPTZ  NOT NULL
);

-- T-02 credentials —— 口令验证材料（6 列，1:1 users；DD-1）
CREATE TABLE credentials (
  uid         BIGINT       PRIMARY KEY REFERENCES users(uid) ON DELETE CASCADE,  -- FK-01
  secret_hash BYTEA        NOT NULL,
  salt        BYTEA        NOT NULL,
  kdf         VARCHAR(16)  NOT NULL DEFAULT 'scrypt',
  iterations  INTEGER      NOT NULL,
  updated_at  TIMESTAMPTZ  NOT NULL
);

-- T-03 usage_counters —— 窗口用量（4 列，1:1 users）
CREATE TABLE usage_counters (
  uid       BIGINT      PRIMARY KEY REFERENCES users(uid) ON DELETE CASCADE,     -- FK-02
  win_start TIMESTAMPTZ NOT NULL,
  requests  INTEGER     NOT NULL DEFAULT 0,
  instr     BIGINT      NOT NULL DEFAULT 0
);

-- T-05 workspaces —— 工作区（9 列；先于 sessions 建表以满足外键顺序）
CREATE TABLE workspaces (
  ws_id        BIGINT      PRIMARY KEY,
  owner_id     BIGINT      NOT NULL REFERENCES users(uid) ON DELETE CASCADE,     -- FK-05
  name         VARCHAR(128) NOT NULL,                 -- DD-7
  version      INTEGER     NOT NULL DEFAULT 1,
  program_blob JSONB,
  config_blob  JSONB       NOT NULL,
  size_bytes   BIGINT      NOT NULL DEFAULT 0,
  created_at   TIMESTAMPTZ NOT NULL,
  updated_at   TIMESTAMPTZ NOT NULL,
  UNIQUE (owner_id, name)                             -- IX-04
);

-- T-04 sessions —— 会话审计（8 列；不参与活跃判定，7.1.3）
CREATE TABLE sessions (
  token      CHAR(43)    PRIMARY KEY,                 -- 32 字节随机数的 base64url，恰好 43 字符
  owner_id   BIGINT      NOT NULL REFERENCES users(uid) ON DELETE CASCADE,       -- FK-03
  ws_id      BIGINT               REFERENCES workspaces(ws_id) ON DELETE SET NULL, -- FK-04
  isa_id     VARCHAR(64),
  created_at TIMESTAMPTZ NOT NULL,
  last_seen  TIMESTAMPTZ NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,                    -- 写行时算好（数据设计 G-4）
  ended_at   TIMESTAMPTZ
);

-- T-06 test_suites —— 用例集（8 列；n:1，ws_id 不加唯一索引，DD-8）
CREATE TABLE test_suites (
  suite_id   BIGINT       PRIMARY KEY,
  owner_id   BIGINT       NOT NULL REFERENCES users(uid) ON DELETE CASCADE,      -- FK-06
  ws_id      BIGINT                REFERENCES workspaces(ws_id) ON DELETE SET NULL, -- FK-07
  name       VARCHAR(128) NOT NULL,
  grp        VARCHAR(64),
  tags       JSONB,
  checksum   VARCHAR(64)  NOT NULL,
  updated_at TIMESTAMPTZ  NOT NULL
);

-- T-07 test_cases —— 用例（9 列）
CREATE TABLE test_cases (
  case_id       BIGINT       PRIMARY KEY,
  suite_id      BIGINT       NOT NULL REFERENCES test_suites(suite_id) ON DELETE CASCADE, -- FK-08
  owner_id      BIGINT       NOT NULL,                -- 冗余谓词列
  name          VARCHAR(128) NOT NULL,
  program_hash  VARCHAR(64),
  timeout_steps BIGINT       NOT NULL,
  expect_mode   SMALLINT     NOT NULL,                -- E-07
  expect_blob   JSONB,
  seq_no        INTEGER      NOT NULL
);

-- T-08 test_reports —— 测试报告汇总（7 列）
CREATE TABLE test_reports (
  report_id   BIGINT      PRIMARY KEY,
  owner_id    BIGINT      NOT NULL REFERENCES users(uid) ON DELETE CASCADE,      -- FK-09
  suite_id    BIGINT               REFERENCES test_suites(suite_id) ON DELETE SET NULL, -- FK-10
  started_at  TIMESTAMPTZ NOT NULL,
  finished_at TIMESTAMPTZ NOT NULL,
  total       INTEGER     NOT NULL,
  passed      INTEGER     NOT NULL
);

-- T-09 report_cases —— 报告内的用例结果（7 列；case_id 不设外键，7.3.10）
CREATE TABLE report_cases (
  report_id     BIGINT  NOT NULL REFERENCES test_reports(report_id) ON DELETE CASCADE, -- FK-11
  case_id       BIGINT  NOT NULL,
  owner_id      BIGINT  NOT NULL,
  passed        BOOLEAN NOT NULL,
  first_diff_at BIGINT,
  diff_fields   JSONB,
  snapshot_blob JSONB,                                -- 重字段，列表页不取（DD-3）
  PRIMARY KEY (report_id, case_id)
);

-- T-10 breakpoints —— 断点表（5 列；ws_id 必须进主键，DD-6）
CREATE TABLE breakpoints (
  owner_id BIGINT  NOT NULL REFERENCES users(uid) ON DELETE CASCADE,             -- FK-12
  ws_id    BIGINT  NOT NULL,                          -- 不设外键（整体替换式写入，7.3.11）
  addr     BIGINT  NOT NULL,
  action   SMALLINT NOT NULL DEFAULT 0,
  enabled  BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (owner_id, ws_id, addr)
);

-- T-11 divergences —— 分歧记录与归因（11 列；job_id 为逻辑引用）
CREATE TABLE divergences (
  div_id        BIGINT      PRIMARY KEY,
  owner_id      BIGINT      NOT NULL REFERENCES users(uid) ON DELETE CASCADE,    -- FK-13
  job_id        VARCHAR(32) NOT NULL,                 -- 逻辑引用，无外键
  step_no       BIGINT      NOT NULL,
  pc            BIGINT      NOT NULL,
  field_diffs   JSONB,
  attr_category SMALLINT,
  attr_by       BIGINT,
  attr_at       TIMESTAMPTZ,
  attr_note     TEXT,
  note          TEXT
);

-- ---------------------------------------------------------------- 索引（IX-02 ~ IX-09）
CREATE INDEX ix_sessions_owner    ON sessions(owner_id, last_seen DESC);       -- IX-02
CREATE INDEX ix_sessions_expires  ON sessions(expires_at);                     -- IX-03
CREATE INDEX ix_workspaces_owner  ON workspaces(owner_id, updated_at DESC);    -- IX-05
CREATE INDEX ix_suites_owner      ON test_suites(owner_id, updated_at DESC);   -- IX-06
CREATE INDEX ix_cases_suite       ON test_cases(suite_id, seq_no);             -- IX-07
CREATE INDEX ix_reports_owner     ON test_reports(owner_id, finished_at DESC); -- IX-08
CREATE INDEX ix_div_owner_job     ON divergences(owner_id, job_id);            -- IX-09
