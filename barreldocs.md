# How to use Barrel

## Command structure
`barrel [options] [ (includes | packswith | -p) (directories or files) ]`

### Options

Option | Use
--- | ---
`isolate` or `-i` | Make the package remove its virtual environment after execution.
`include` or `-a` | Include one directory or file in the package
`name` or `-n` | Set the name for the output package

### Includes
After adding `includes`, any parameter after it is a directory or file to include in the final package

Please note that you need to add `/*` after a directory if you want to include things directly inside the it, and use `/**` if you want to incude *everything* inside