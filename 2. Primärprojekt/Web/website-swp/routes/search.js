var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('search', { title: 'Software Projekt WS20/21' , subtitle: 'Bilderweiterung mittels Methoden des maschinellen Lernens'});
});

module.exports = router;
