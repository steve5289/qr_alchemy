## 
# Execution Starts here
function main {
    local BURST_DIR="$1"
    local IMAGE_NAME="$2"
    local DNG_FILE="$2.dng"
    local IMAGE_FILE

    run_stock_postprocess "$@"

    get_image_file "$IMAGE_NAME"
    if [[ -n "$OUTPUT" ]]; then
        IMAGE_FILE="$OUTPUT"
        if [[ "$CLEAN_DNG_FILE" -eq 1 ]]; then
            rm -f "$DNG_FILE"
        fi
    else
        die "Error! Could not find image file with name '$IMAGE_NAME'!"
    fi

    %STANDALONE%/%BUILD_STANDALONE%/qr_alchemy.sh -f "$OUTPUT"
}

##
# As we are only given a image name (no extention like .jpg) we need to figure out what that is.
function get_image_file {
    local IMAGE_NAME="$1"
    local file

    for file in "$IMAGE_NAME."{jpg,tiff,png}; do
        if [[ -e "$file" ]]; then
            OUTPUT="$file"
            return
        fi
    done
}

##
# Run the normal mexgapixels postprocess script so that we don't need to maintain a version of that.
function run_stock_postprocess {
    $STOCK_POSTPROCESS_PATH "$@" || exit $?
}

##
# exit with the given message
function die {
    echo "$@" 1>&2
    exit 2
}

main "$@"

