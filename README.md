# psychopy-mri-emulator

Software emulator for fMRI hardware.

Idea: Run or debug an experiment script using exactly the same code, i.e., for both testing and online data acquisition. 
To debug timing, you can emulate sync pulses and user responses. Limitations: pyglet only; keyboard events only.

## Installing

Install this package with the following shell command:: 

    pip install psychopy-mri-emulator

You may also use PsychoPy's builtin package manager to install this package.

## Usage

Once the package is installed, PsychoPy will automatically load it when started and make objects available within the
`psychopy.hardware.emulator` namespace.

