var express = require("express");
var router = express.Router();
const fs = require('fs'); //TEST
const {execFile} = require("child_process");

router.post("/", function (req, res) {
    const seks_per_mili = 1000;
    const timeout = 1 * seks_per_mili;
    
    setTimeout(() => { 

    function compose(fst, snd) {
        return fst + "_" + snd;
    }
    var inputImg = req.files.inputImg;
    var referenceImg = req.files.referenceImg;
    var referenceExist = !!referenceImg;
    var json = req.body;
    var allDatasets = [];
    var allMethods = [];
    var pstring = "";
    var placeholder_nan = "images/placeholder_nan.png"
    var placeholder_ref = "images/placeholder_ref.png"

    for (pair in json) {
        if (pair.includes('method')) {
            allMethods.push(json[pair]);
        } else if (pair.includes('dataset')) {
            allDatasets.push(json[pair]);
        }
        pstring += json[pair] + " ";
    }

    var args = [
            inputImg.name
            , inputImg.size
            , inputImg.encoding
            , inputImg.mimetype
            , inputImg.tempFilePath
            , referenceExist ? referenceImg.tempFilePath : "False"
            , pstring
    ];

    execFile(
        "public/scripts/parseBody.sh"
        , args
        , (err, stdout, stderr) => {
            var scriptres = stdout.split(" ");
            inputImg.tempFilePath = inputImg.tempFilePath.replace("public/","");
            if (referenceExist) {
                referenceImg.tempFilePath = referenceImg.tempFilePath.replace("public/","");
            }

            var results = {};
            scriptres.forEach((p) => {
                // should parse NaN
                p = JSON.parse(p);
                if (results[p.method] == undefined) {
                    results[p.method] = {};
                }
                results[p.method][p.dataset] = {
                    img: isNaN(p.runtime) ? placeholder_nan : compose(compose(inputImg.tempFilePath, p.method), p.dataset)
                    , runtime: p.runtime
                    , norm: p.norm
                };
            }); 

            res.render("results", {
                title: "Software Projekt WS20/21",
                subtitle: 'Bilderweiterung mittels Methoden des maschinellen Lernens',
                userInput: inputImg.tempFilePath,
                userReference: referenceExist ? referenceImg.tempFilePath : placeholder_ref,
                methods: allMethods,
                datasets: allDatasets,
                data: results    
            });
        }
    );
}, timeout);
});

module.exports = router;
