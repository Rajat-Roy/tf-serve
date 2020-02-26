# tf-serve

# Download the TensorFlow Serving Docker image and repo
```bash
docker pull tensorflow/serving

wget https://github.com/Rajat-Roy/tf-serve/releases/download/v1/mobilenet.zip

unzip mobilenet.zip

docker run -p 8501:8501 \
  --mount type=bind,source=$(pwd)/mobilenet,target=/models/mobilenet \
  -e MODEL_NAME=mobilenet -t tensorflow/serving
```
  
# Configure Server App
```bash
sudo apt install python3-venv
mkdir my_flask_app
cd my_flask_app
python3 -m venv venv
source venv/bin/activate
pip install Flask
python -m flask --version

export FLASK_APP=server
flask run --host=0.0.0.0
```
  
