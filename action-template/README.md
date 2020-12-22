# Github Actions with Python

This is a template to setup a Github Action using Python. It is as minimal as 
possible, but very powerful. Essentially, you just need to write a python script
to do cool stuff. The rest should work.

### Steps

1. Copy the `action-template` folder structure and contents to the repository that
will host the action. You should place it under `.github/workflows/`

2. Change the name of your action. In this case, whatever has `action-name`.

3. Edit `action-name.yml` to perform the steps that you want to. Remember to
set up the trigger!

4. Edit your `main.py` script to do whatever you want. Tip: if you need an external
variable use `with` or `env` in `action-name.yml`.

5. Push the changes and perform the action in your repo. Check out the results,
fix the errors and repeat.
