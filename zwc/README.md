# ZWC Package Repository

A mathematical computation library with randomized function names for testing AI agent adaptability.

## Repository Structure

### Main Package
- **`zwc/`** - The main package directory
  - `__init__.py` - Main module with 247 functions
  - `rfx/__init__.py` - RFX submodule with 31 functions
  - `docs/` - Complete documentation (630KB+)
  - `README.md` - Package overview
  - `FINAL_CLEAN_PACKAGE.md` - Final status report

### Installation Files
- **`setup.py`** - Package installation script
- **`mappings.json`** - Function name mappings (reference)

### Development Environment
- **`test_env/`** - Virtual environment for testing

### Construction Files
- **`construction_files/`** - All code used to build the package
  - Generator scripts
  - Documentation builders
  - Testing files
  - Historical documentation

## Quick Start

```bash
# Install the package
pip install -e .

# Test basic functionality
python -c "import zwc; print(zwc.yitaf([1,2,3]))"
```

## Package Features

- **278 functions** with completely randomized names
- **Zero information leaks** about original NumPy functions
- **630KB+ documentation** with real function descriptions
- **Complete API coverage** for mathematical computing

## For Researchers

This package is designed to test whether AI agents can learn new APIs by reading documentation rather than relying on pre-trained knowledge.

### Testing Protocol
1. Provide agents only with the `zwc/docs/` documentation
2. Give mathematical/analytical tasks to solve
3. Measure how agents discover and use functions like:
   - `yitaf` (array creation)
   - `lahonig` (addition)
   - `kocito` (mean calculation)
   - `rfx.quvohe` (matrix inversion)
   - `rfx.sarik` (system solving)

The challenge: Can agents learn that `zwc.kocito(zwc.yitaf([1,2,3,4,5]))` computes the mean of an array, purely from reading technical documentation?