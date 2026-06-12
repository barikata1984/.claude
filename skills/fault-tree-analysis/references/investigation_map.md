# Investigation Map

A mapping from cause categories to concrete investigation actions. Use this as a
reference during Phase 4 to choose the right tool for each hypothesis.

## 1. Logic Error

| Action | When to use | What it tells you |
|--------|------------|-------------------|
| Read the suspect function | First pass on any logic hypothesis | Whether the algorithm/condition is correct |
| Write a minimal reproducing test | When you have a specific input that should fail | Isolates the logic from environment/state |
| Check git blame / git log | When suspecting a regression | Whether the code changed recently |
| Add assertions at intermediate steps | When a long function produces wrong output | Where the computation first diverges |
| Trace with print/log statements | When control flow is unclear | Which branch was actually taken |

## 2. State Corruption

| Action | When to use | What it tells you |
|--------|------------|-------------------|
| Log variable values at function entry/exit | When suspecting stale or wrong state | Whether state is what you expect at each boundary |
| Search for global/module-level mutable state | When state seems to "leak" between calls | Whether shared state exists |
| Check initialization order | When bug appears only on first run or after reset | Whether init is incomplete or misordered |
| Run the same operation twice in sequence | When suspecting cache staleness | Whether results differ (indicates stale state) |

## 3. Race Condition

| Action | When to use | What it tells you |
|--------|------------|-------------------|
| Add timing logs around suspect sections | When bug is intermittent | Whether timing correlates with failures |
| Search for shared mutable state across threads | First pass on concurrency hypothesis | Whether a data race is structurally possible |
| Review lock/synchronization code | When shared state is confirmed | Whether synchronization is correct |
| Run under thread sanitizer (if available) | When data race is suspected | Definitive detection of unsynchronized access |
| Insert artificial delays (sleep) | When trying to widen a timing window | Whether the bug becomes reproducible |

## 4. Configuration

| Action | When to use | What it tells you |
|--------|------------|-------------------|
| Print resolved config values at runtime | First pass on any config hypothesis | What the code actually sees (vs. what you think) |
| Diff config across working/failing environments | When bug is environment-specific | Which config values differ |
| Check environment variables | When config comes from env | Whether expected vars are set and correct |
| Temporarily hardcode the expected value | When suspecting a specific config key | Whether that config key is the cause |

## 5. Dependency

| Action | When to use | What it tells you |
|--------|------------|-------------------|
| Check installed versions (pip freeze, npm ls) | First pass on dependency hypothesis | Whether versions match expectations |
| Read dependency changelog | When version differs from expected | Whether breaking changes were introduced |
| Test with pinned known-good version | When suspecting a version regression | Whether the old version works |
| Check external service health | When depending on network services | Whether the service is responsive and correct |
| Review API contract / type stubs | When suspecting interface mismatch | Whether your usage matches the current API |

## 6. Data

| Action | When to use | What it tells you |
|--------|------------|-------------------|
| Log input data shape, type, and range | First pass on any data hypothesis | Whether input matches assumptions |
| Test with known-good input data | When suspecting data corruption | Whether the code works with clean data |
| Check for null/empty/NaN values | When output is wrong or missing | Whether unexpected missing values propagate |
| Validate schema at entry point | When data crosses a boundary (API, file, DB) | Whether the contract is honored |
| Check encoding (UTF-8, line endings) | When string processing behaves oddly | Whether encoding assumptions hold |

## 7. Environment

| Action | When to use | What it tells you |
|--------|------------|-------------------|
| Compare OS and runtime versions | When bug is environment-specific | Whether a platform difference explains it |
| Test in the failing environment | When "works on my machine" | Whether the bug is environment-dependent |
| Check filesystem permissions | When file operations fail | Whether access rights differ |
| Compare container images / Dockerfiles | When dev vs. CI/staging differ | Whether the runtime environment matches |
| Check PATH and dynamic library resolution | When binaries behave differently | Whether the right executables are found |

## 8. Resource Exhaustion

| Action | When to use | What it tells you |
|--------|------------|-------------------|
| Monitor memory usage during reproduction | When suspecting OOM | Whether memory grows unboundedly |
| Check disk space | When file writes fail silently | Whether disk is full |
| Check connection pool / fd limits | When network operations fail intermittently | Whether resources are exhausted |
| Profile allocation patterns | When memory grows slowly | Where allocations happen |
| Check ulimit / cgroup constraints | When running in containers | Whether resource limits are hit |

## Cross-Branch Investigation Strategies

These actions are especially valuable because they provide evidence about multiple
branches simultaneously:

| Action | Branches it addresses |
|--------|----------------------|
| Reproduce in a clean/fresh environment | Configuration, Environment, Dependency |
| Reproduce with minimal input | Data, Logic Error, Resource Exhaustion |
| Check git log for recent changes | Logic Error (regression), Configuration, Dependency |
| Run the existing test suite | Logic Error, State Corruption, Dependency |
| Binary search with git bisect | All categories (identifies the introducing commit) |
