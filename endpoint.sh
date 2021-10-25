git reset --hard HEAD
git pull
docker rm -f bcb
docker build -t blockchainbot:latest .
docker run -itd --rm  --name bcb -p 50006:5000
