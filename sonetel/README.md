<br />
<div align="center">
  <a href="https://github.com/Sonetel/sonetel-python">
    <img src="https://dl.dropboxusercontent.com/s/hn4o0v378od1aoo/logo_white_background.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Sonetel API Python Wrapper</h3>

<p align="center">
    A Python package to use Sonetel's REST APIs.
    <br />
    <br />
    <a href="https://sonetel.com/en/developer/">Sonetel Developer Home</a>
    .
    <a href="https://sonetel.com/en/developer/api-documentation/">API Documentation</a>
    .
    <a href="https://app.sonetel.com/register?tag=api-developer&simple=true">Get Free Account</a>
  </p>
</div>

## Build from source
 + Follow [these instructions](https://packaging.python.org/en/latest/tutorials/packaging-projects/) to get the latest build tools.
 + `git clone https://github.com/Sonetel/sonetel-python.git`
 + `cd sonetel-python`.
 + `py -m build`

## Install
To install the module built locally:
+ Copy the `sonetel-<VERSION>.tar.gz` file from the `dist/` folder into your project folder.
+ Run the command `pip install sonetel-<VERSION>.tar.gz`
+ To import in your script, use `import sonetel as sntl`.
  + Alternatively, to use specific resources such as Auth use `from sonetel import Auth`
