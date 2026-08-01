
#How to install dependecies
cd  sjinvoc
pip install -r requirements/producation.txt
pip install -r requirements/base.txt
pip install -r requirements/local.txt
#If testing
pip install -r requirements/tests.txt


## Django Environment Configuration

The project uses the `DJANGO_ENV` environment variable to switch between development and production settings.

### Development Environment

Set the environment variable:

```bash
export DJANGO_ENV=development