-- ============================================================================
-- ISA 模拟系统 —— SQLite 形态的库结构（11 张表 / 83 列 / 13 个外键 / 9 个索引）
--
-- 设计依据：《软件详细设计文档》7.3（T-01 ~ T-11、FK-01 ~ FK-13、IX-01 ~ IX-09）
-- 说明：双形态同源（SA-09），9 个逻辑类型 / 7 处 DDL 差异由 DbDriver 吸收（7.2.2）。
--       本文件是 SQLite 侧的落地形态：TIMESTAMPTZ → TEXT，BYTEA/BLOB，JSONB → TEXT。
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 版本表：启动序列统一检查（7.4.6）
CREATE TABLE schema_version (
  version INTEGER NOT NULL
);

-- T-01 users —— 用户身份、角色、配额、状态（9 列）
CREATE TABLE users (
  uid         INTEGER PRIMARY KEY,                    -- 由 IIdGen 生成（G-2），不用自增
  username    TEXT    NOT NULL UNIQUE,                -- IX-01
  role        INTEGER NOT NULL DEFAULT 0,             -- E-18：0 = User, 1 = Admin
  q_sessions  INTEGER NOT NULL DEFAULT 64,
  q_requests  INTEGER NOT NULL DEFAULT 600,
  q_instr     INTEGER NOT NULL DEFAULT 10000000,      -- NFR-Q5
  q_bytes     INTEGER NOT NULL DEFAULT 67108864,      -- 64 MiB
  status      INTEGER NOT NULL DEFAULT 0,             -- E-19：0 = Active, 1 = Disabled
  created_at  TEXT    NOT NULL
);

-- T-02 credentials —— 口令验证材料（6 列，1:1 users；DD-1 凭据与身份分表）
CREATE TABLE credentials (
  uid         INTEGER PRIMARY KEY REFERENCES users(uid) ON DELETE CASCADE,  -- FK-01
  secret_hash BLOB    NOT NULL,                       -- KDF 输出
  salt        BLOB    NOT NULL,                       -- 每用户独立随机盐
  kdf         TEXT    NOT NULL DEFAULT 'scrypt',      -- 字符串而非枚举：换算法只写新值
  iterations  INTEGER NOT NULL,                       -- 成本参数随行存储，便于逐用户升级
  updated_at  TEXT    NOT NULL
);

-- T-03 usage_counters —— 窗口用量（4 列，1:1 users）
-- Usage.sessions / Usage.bytes 为派生值，不落列（DD-4）
CREATE TABLE usage_counters (
  uid       INTEGER PRIMARY KEY REFERENCES users(uid) ON DELETE CASCADE,    -- FK-02
  win_start TEXT    NOT NULL,
  requests  INTEGER NOT NULL DEFAULT 0,
  instr     INTEGER NOT NULL DEFAULT 0
);

-- T-05 workspaces —— 工作区（9 列）
-- suite_blob 已弃用（DD-2）：用例集落子表
CREATE TABLE workspaces (
  ws_id       INTEGER PRIMARY KEY,
  owner_id    INTEGER NOT NULL REFERENCES users(uid) ON DELETE CASCADE,     -- FK-05
  name        TEXT    NOT NULL,                       -- DD-7：UC-12 E1 同名冲突判定
  version     INTEGER NOT NULL DEFAULT 1,             -- 乐观并发（7.4.5）
  program_blob TEXT,                                  -- 0..1（选择性保存时程序可缺席）
  config_blob TEXT    NOT NULL,                       -- SessionConfig，恒有值
  size_bytes  INTEGER NOT NULL DEFAULT 0,             -- Usage.bytes 的来源
  created_at  TEXT    NOT NULL,
  updated_at  TEXT    NOT NULL,
  UNIQUE (owner_id, name)                             -- IX-04：复合唯一（不同用户可同名）
);

-- T-04 sessions —— 会话审计（8 列）
-- 注意：本表只作审计与统计，不参与活跃判定；live_ 恒从空开始（7.1.3）
CREATE TABLE sessions (
  token      TEXT    PRIMARY KEY,                     -- 32 字节随机数的 base64url（43 字符）
  owner_id   INTEGER NOT NULL REFERENCES users(uid) ON DELETE CASCADE,      -- FK-03
  ws_id      INTEGER          REFERENCES workspaces(ws_id) ON DELETE SET NULL, -- FK-04
  isa_id     TEXT,                                    -- ISA 描述不落库，故只存标识、不设外键
  created_at TEXT    NOT NULL,
  last_seen  TEXT    NOT NULL,
  expires_at TEXT    NOT NULL,                        -- last_seen + sessionTimeout，写行时算好（G-4）
  ended_at   TEXT                                     -- dropSession 写入；为空表示未正常结束
);

-- T-06 test_suites —— 用例集（8 列）
-- 基数 n:1（DD-8，用户裁决）：一个工作区可挂多个用例集，故 ws_id 不加唯一索引
CREATE TABLE test_suites (
  suite_id   INTEGER PRIMARY KEY,
  owner_id   INTEGER NOT NULL REFERENCES users(uid) ON DELETE CASCADE,      -- FK-06
  ws_id      INTEGER          REFERENCES workspaces(ws_id) ON DELETE SET NULL, -- FK-07
  name       TEXT    NOT NULL,
  grp        TEXT,                                    -- group 是保留字，故改名（7.3.1）
  tags       TEXT,                                    -- JSON 字符串数组
  checksum   TEXT    NOT NULL,                        -- C-12 完整性校验
  updated_at TEXT    NOT NULL
);

-- T-07 test_cases —— 用例（9 列）
CREATE TABLE test_cases (
  case_id       INTEGER PRIMARY KEY,
  suite_id      INTEGER NOT NULL REFERENCES test_suites(suite_id) ON DELETE CASCADE,  -- FK-08（组合）
  owner_id      INTEGER NOT NULL,                     -- 冗余谓词列：便于 report_cases 直接隔离
  name          TEXT    NOT NULL,
  program_hash  TEXT,
  timeout_steps INTEGER NOT NULL,
  expect_mode   INTEGER NOT NULL,                     -- E-07（DiffMode）
  expect_blob   TEXT,                                 -- ExpectedSpec 联合类型整体序列化
  seq_no        INTEGER NOT NULL                      -- 用例集内执行顺序（NFR-Q2）
);

-- T-08 test_reports —— 测试报告汇总（7 列）
-- passRate 由 passed / total 现算，不存冗余百分比
CREATE TABLE test_reports (
  report_id   INTEGER PRIMARY KEY,
  owner_id    INTEGER NOT NULL REFERENCES users(uid) ON DELETE CASCADE,     -- FK-09
  suite_id    INTEGER          REFERENCES test_suites(suite_id) ON DELETE SET NULL, -- FK-10
  started_at  TEXT    NOT NULL,
  finished_at TEXT    NOT NULL,
  total       INTEGER NOT NULL,
  passed      INTEGER NOT NULL
);

-- T-09 report_cases —— 报告内的用例结果（7 列）
-- case_id 不设外键：用例集可被删除或覆盖，而历史报告必须保留（7.3.10）
CREATE TABLE report_cases (
  report_id     INTEGER NOT NULL REFERENCES test_reports(report_id) ON DELETE CASCADE, -- FK-11（组合）
  case_id       INTEGER NOT NULL,
  owner_id      INTEGER NOT NULL,                     -- 冗余谓词列
  passed        INTEGER NOT NULL,                     -- BOOLEAN：SQLite 存 0/1
  first_diff_at INTEGER,
  diff_fields   TEXT,                                 -- JSON 数组
  snapshot_blob TEXT,                                 -- 重字段，列表页不取（DD-3）
  PRIMARY KEY (report_id, case_id)
);

-- T-10 breakpoints —— 断点表（5 列）
-- ws_id 必须进主键（DD-6）：saveBreakpoints 签名无工作区维度，靠它提供归属
CREATE TABLE breakpoints (
  owner_id INTEGER NOT NULL REFERENCES users(uid) ON DELETE CASCADE,        -- FK-12
  ws_id    INTEGER NOT NULL,                          -- 不设外键（整体替换式写入，7.3.11）
  addr     INTEGER NOT NULL,
  action   INTEGER NOT NULL DEFAULT 0,                -- 命中动作；本期恒为 0
  enabled  INTEGER NOT NULL DEFAULT 1,
  PRIMARY KEY (owner_id, ws_id, addr)
);

-- T-11 divergences —— 分歧记录与归因（11 列）
-- job_id 为逻辑引用（任务不落库），故无外键；sideA / sideB 完整快照不持久化（7.3.12）
CREATE TABLE divergences (
  div_id        INTEGER PRIMARY KEY,
  owner_id      INTEGER NOT NULL REFERENCES users(uid) ON DELETE CASCADE,   -- FK-13
  job_id        TEXT    NOT NULL,                     -- 逻辑引用
  step_no       INTEGER NOT NULL,
  pc            INTEGER NOT NULL,
  field_diffs   TEXT,                                 -- JSON 数组
  attr_category INTEGER,                              -- E-08（AttributionCategory）
  attr_by       INTEGER,
  attr_at       TEXT,
  attr_note     TEXT,
  note          TEXT
);

-- ---------------------------------------------------------------- 索引（IX-02 ~ IX-09）
-- IX-01 已由 users.username 的 UNIQUE 提供，IX-04 由复合 UNIQUE 提供
CREATE INDEX ix_sessions_owner    ON sessions(owner_id, last_seen DESC);      -- IX-02
CREATE INDEX ix_sessions_expires  ON sessions(expires_at);                    -- IX-03
CREATE INDEX ix_workspaces_owner  ON workspaces(owner_id, updated_at DESC);   -- IX-05
CREATE INDEX ix_suites_owner      ON test_suites(owner_id, updated_at DESC);  -- IX-06
CREATE INDEX ix_cases_suite       ON test_cases(suite_id, seq_no);            -- IX-07
CREATE INDEX ix_reports_owner     ON test_reports(owner_id, finished_at DESC);-- IX-08
CREATE INDEX ix_div_owner_job     ON divergences(owner_id, job_id);           -- IX-09
