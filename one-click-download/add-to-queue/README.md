Create env with

`make create-env`

Run application

`. .add-to-queue/bin/activate; python enqueue.py`

In the `enqueue.py` file, you have to edit

```
main_project_path # Path with all metadata
credentials_path  # Path with gcloud service account json credential file
runall            # Boolean to run all datasets and tables
```