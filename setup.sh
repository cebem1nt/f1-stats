DB_SOURCE="https://github.com/f1db/f1db/releases/download/v2026.0.0.beta1/f1db-sqlite.zip"
DB_NAME="f1db.db"

mkdir -p data

if [[ ! -e "data/$DB_NAME" ]]; then
    wget $DB_SOURCE -P data
    unzip data/f1db-sqlite.zip -d data/
    rm data/f1db-sqlite.zip
fi