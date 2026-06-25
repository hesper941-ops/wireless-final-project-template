# AI Log

## Prompt 1

User prompt: create a minimal testable Python project skeleton based on
`DESIGN.md` and `TEST_PLAN.md`, without implementing the final complete system.

AI-generated content:

- Added `main.py` CLI skeleton.
- Added modular files under `src/`.
- Added `tests/test_mock_stage1.py` with seven mock tests.

Manual changes and review:

- Verified the QPSK Gray mapping manually against the PRD.
- Ran `pytest tests -q` and confirmed the first-stage mock tests passed.

Adoption reason:

- The skeleton matched the documented module boundaries and avoided hard-coded
  `Test.txt` content.

## Prompt 2

User prompt: write a mock test report describing test purpose, environment,
seven mock tests, test result, found issue, design revision, and conclusion.

AI-generated content:

- Added `MOCK_TEST_REPORT.md`.
- Recorded that `main.py` was still a placeholder after Stage 1.
- Recorded the next-stage plan for `received.txt`, `metrics.json`, and plots.

Manual changes and review:

- Checked that the report clearly stated Stage 1 scope and did not claim final
  end-to-end recovery.

Adoption reason:

- The report documents the transition from mock testing to full system
  implementation.

## Prompt 3

User prompt: implement the complete end-to-end wireless communication file
transmission system without breaking the seven mock tests.

AI-generated content:

- Added `src/pipeline.py`, `src/metrics.py`, `src/plots.py`, and `src/utils.py`.
- Updated `main.py` to run the full chain.
- Generated `results/received.txt`, `results/metrics.json`, and three plots.

Manual changes and review:

- Verified byte-level equality between `Test.txt` and `results/received.txt`.
- Ran `pytest tests -q`.
- Ran the required CLI command at SNR = 12 dB and seed = 2026.

Adoption reason:

- The complete chain produced exact recovery at the baseline condition while
  preserving the Stage 1 unit-test interfaces.

## Prompt 4

User prompt: inspect Windows file writing, image saving, and result generation
logic, especially why the `results/` directory cannot be deleted by pytest
fixtures.

AI-generated content:

- Changed plot saving to write Matplotlib figures into an in-memory PNG buffer.
- Closed figures with `plt.close(fig)` and `plt.close("all")`.
- Wrote PNG bytes with `Path.write_bytes`.

Manual changes and review:

- Confirmed that text and JSON outputs use `Path.write_bytes` and
  `Path.write_text`.
- Confirmed no explicit file handle is kept open under `results/`.
- Checked Windows file attributes and ACL information for generated PNG files.

Adoption reason:

- The buffer-based save path minimizes file-handle risk and makes result
  generation easier to reason about on Windows.
