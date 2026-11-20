# s3filesstreamlit

### Docker commands to run the application
```bash
docker build -t s3files-streamlit .

mkdir -p ./test-data

docker run --rm \
  -p 8501:8501 \
  -v "$(pwd)/test-data:/mnt/s3files" \
  s3files-streamlit
```