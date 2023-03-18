#/!bin/bash

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
# This script's purpose is to serve as a helper
# for our web application. It's used to parse the
# request body, serve the necessary params to
# our model caller and then serve the result
# back to the application.
#
# Const
# =====
# CROPPED, image size for testimgs
# FULLSIZE, Size models were trained on
# MODELCS, call script for models
# APPIMG, Path to Singularity app image
# PRE, Imagefile  prefix
# 
#
# Params
# ======
# $1..4 inputImg properties name, size, enoding, mimetype
# $5, tempFilePath inputImg
# $6, tempFilePath reference or False
# $7..N methods, datasets (order doesn't matter)
#
# Returns
# =======
# json objects on stdout
# method: curr_method
# dataset: curr_dataset
# norm: float, result frobeniusnorm
# runtime: float, time per execution
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#

CROPPED='40x49'
FULLSIZE='62x75'
PRE='public/uploads/'
APPIMG='/data/models/appImage'
MODELCS="python3 /data/models"
DEBUGSTR="${1} ${4} ${2}B ${3}"
shift 4

function img_convert() {
  if [ "False" == "${1}" ]; then
    return 0
  elif [ ! -f ${1}_unconv ]; then
    cp $1 ${1}_unconv
  fi
  convert $1 -resize ${2} $1
#  public/scripts/aspectcrop -a $(echo $2 | sed 's/x/:/') -g c $1 ${1}_cropped
#  mv ${1}{_cropped,}
#convert $1 -gravity center -extend $2 -background white -flatten $1
  return 1
}

# No matter what size the images had before we assure that
# they're in the right shape, so we resize it using convert
img_convert $1 $CROPPED
img_convert $2 $FULLSIZE
if [ 0 -eq $? ]; then
  NOREF=1
fi
#if [ ! -f ${1}_unconv ];  then
#  cp ${1} ${1}_unconv
#fi
#convert $1 -resize $CROPPED $1
#if [ "$2" != "False" ]; then
#  if [ ! -f ${2}_unconv ];  then
#    cp ${2} ${2}_unconv
#  fi
#  convert $2 -resize $FULLSIZE $2
#else
#  NOREF=1
#fi

# remove imagepath so only filename stays for the models
IMGI=$(echo $1 | sed "s@$PRE@@g")
if [ -z $NOREF ]; then
  IMGR=$(echo $2 | sed "s@$PRE@@g")
else
  IMGR="False"
fi

shift 2

arrM=""
arrD=""
while [ $# -gt 0 ]; do
  arrM="$arrM $(echo $1 | grep -oE '[a-zA-Z]+')"
  arrD="$arrD $(echo $1 | grep -oE '[0-9]+')"
  shift
done

# since best would be parsed as a model we have to search for it and 
# move it as a dataset if necessary. grep returns 0 on a match, otherwise != 0
$(echo "${arrM}" | grep best 2>&1 >/dev/null)
if [ 0 -eq $(echo $?) ]; then
  arrM=$(echo $arrM | sed 's/best//')
  arrD="$arrD best"
  BESTMODE=1
fi

RESULT=""
for m in ${arrM[*]}; do
  for d in ${arrD[*]}; do
      TMOD="${MODELCS}/${m}/predict.py"
      CUR=$(bash -c "${TMOD} ${IMGI} ${IMGR} ${d}")
          
# gather runtime (and frobenius norm froms stdin
# if only rt is given, N will be empty
      if [ -z "$CUR" ]; then
        RT=\"NaN\"
        N=\"NaN\"
        echo "$(date) [${DEBUGSTR}]:: ${TMOD} ${IMGI} ${IMGR} ${d}" >> /var/log/swp/npm/crash.log
      else
        RT=$(echo $CUR | cut -d' ' -f1)
        N=$(echo $CUR | sed -E "s/$RT ?//" )
        if [ -z $N ]; then
            N=0
        fi
      fi

# glue together a String of json objects space separated to
# easily split it into an array
      RESULT="$RESULT {\"method\":\"${m}\",\"dataset\":${d},\"norm\":${N},\"runtime\":${RT}}"
  done
done

# JSON could not parse best without surrounding (double) quotes
if [ ! -z "$BESTMODE" ]; then
  RESULT=$(echo "${RESULT}" | sed 's/best/\"best\"/g')
fi

# do not remove '-n' otherwise you would get a json array with last entry has
# trailing '\n'
echo -n ${RESULT}
