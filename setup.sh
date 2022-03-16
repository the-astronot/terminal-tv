# Setup Script for Terminal-TV

# Install required modules
pip3 install -r requirements.txt

# DEFAULTS
# Can be modified and run again, or changed in src/.env
MEDIA_FOLDER="media/"
DELIMITER=","
TERM_WIDTH="160"
FPS="15"
COLOR_OFFSET="15"

# Create .env file
cat > src/.env <<EOT
MEDIA_LOCATION=$(pwd)/$MEDIA_FOLDER
DELIMITER=$DELIMITER
TERM_WIDTH=$TERM_WIDTH
FPS=$FPS
COLOR_OFFSET=$COLOR_OFFSET
EOT

# Create Media Folder
# This is where the converter will store
# and the player will look for files
if ! [[ -d $MEDIA_FOLDER ]]
then
	mkdir $MEDIA_FOLDER
fi

# Create Config Foler
if ! [[ -d "configs/" ]]
then
	mkdir "configs/"
fi
