### Download and Setup MongoDB
1. Download "MongoDB Community Server" (eg. [mongodb-macos-arm64-8.0.10](https://fastdl.mongodb.org/osx/mongodb-macos-arm64-8.0.10.tgz))
2. Move "MongoDB Community Server" to home folder
```bash
mv mongodb-macos-arm64-8.0.10 /User/${user_name}
```
3. Add mongodb/bin path to .zshrc
```bash
vi ~/.zshrc
export PATH=${PATH}:/User/${user_name}/mongodb-macos-arm64-8.0.10/bin
source ~/.zshrc
```
4. Create /data/db folder into home folder
```bash
cd ~
sudo mkdir -p /data/db
```
5. Run MongoDB server
```bash
sudo mongod --dbpath=/Users/${user_name}/data/db
```

### Setup Python Environment
1. Create virtual environment
```bash
conda create --name trip-planner python=3.10
```
```bash
conda activate trip-planner
```
2. install packages

```bash
pip install flask pymongo
```
