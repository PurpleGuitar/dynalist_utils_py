#!/usr/bin/env bash

# This is a convenience script for creating HTML and PDF from DynaList
# using Pandoc.
#
# - You may need a more recent version of Pandoc than comes with your
#   system to support HTML->PDF with stylesheets.
# - Set the DL2MD_OUTPUT_FOLDER to the absolute path of your output folder.
# - You may set DL2MD_OUTPUT_FILENAME if you wish, default 'dl2md'
# - Requires xclip to copy Dynalist URL from the clipboard.
# - PDF creation requires wkhtmltopdf to be installed.

# Verify output folder
if [ -z "$DL2MD_OUTPUT_FOLDER" ]; then
    echo "ERROR: Please set DL2MD_OUTPUT_FOLDER."
    exit 1
fi

# Copy Dynalist URL from clipboard if not already set
if [ -z "$DL2MD_DYNALIST_URL" ]; then
    export DL2MD_DYNALIST_URL="$(xclip -o)"
fi

# Validate Dynalist URL
if [[ "${DL2MD_DYNALIST_URL}" =~ ^https://dynalist.io/d ]]; then
    echo "Dynalist URL: ${DL2MD_DYNALIST_URL}"
else
    echo "URL doesn't look like a Dynalist URL.  Try copying from your browser or setting DL2MD_DYNALIST_URL."
    echo "URL: ${DL2MD_DYNALIST_URL}"
    exit 1
fi

# Get directory of this script
# from: https://stackoverflow.com/a/246128
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

# Check for custom filename
if [ -z "$DL2MD_OUTPUT_FILENAME" ]; then
    export DL2MD_OUTPUT_FILENAME="dl2md"
fi

# Copy stylesheet if needed
STYLESHEET_SOURCE_FILENAME="${DIR}/dl2md.css"
STYLESHEET_TARGET_FILENAME="${DL2MD_OUTPUT_FOLDER}/${DL2MD_OUTPUT_FILENAME}.css"
if [ ! -f "${STYLESHEET_TARGET_FILENAME}" ]; then
    cp ${STYLESHEET_SOURCE_FILENAME} ${STYLESHEET_TARGET_FILENAME}
fi

# Create json file from Dynalist
${DIR}/../dlget/dlget \
    --url "${DL2MD_DYNALIST_URL}" \
    --outfile "${DL2MD_OUTPUT_FOLDER}/${DL2MD_OUTPUT_FILENAME}.json"

# Create md file from Dynalist
${DIR}/dl2md \
    --url "${DL2MD_DYNALIST_URL}" \
    --outfile "${DL2MD_OUTPUT_FOLDER}/${DL2MD_OUTPUT_FILENAME}.md"

# Create html file
pandoc \
    --standalone \
    --css ${DL2MD_OUTPUT_FILENAME}.css \
    --output "${DL2MD_OUTPUT_FOLDER}/${DL2MD_OUTPUT_FILENAME}.html" \
    "${DL2MD_OUTPUT_FOLDER}/${DL2MD_OUTPUT_FILENAME}.md" \

# Create PDF file
pandoc \
    --standalone \
    --css "${DL2MD_OUTPUT_FOLDER}/${DL2MD_OUTPUT_FILENAME}.css" \
    --variable papersize=Letter \
    --variable margin-left=1in \
    --variable margin-right=1in \
    --variable margin-top=1in \
    --variable margin-bottom=1in \
    --pdf-engine=wkhtmltopdf \
    --output "${DL2MD_OUTPUT_FOLDER}/${DL2MD_OUTPUT_FILENAME}.pdf" \
    "${DL2MD_OUTPUT_FOLDER}/${DL2MD_OUTPUT_FILENAME}.md" \
