var createError = require('http-errors');
var express = require('express');
var path = require('path');
var upload = require('express-fileupload');
var hbs = require('hbs');
var searchRouter = require('./routes/search');
var getResultsRouter = require('./routes/getResults');
var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');

app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'public')));

/*****************************************************************************\
|* see https://github.com/richardgirges/express-fileupload#available-options *|
|* and            https://github.com/mscdex/busboy#busboy-methods            *|
\*****************************************************************************/
app.use(upload({
        useTempFiles: true
        , tempFileDir: 'public/uploads/'
        , createParentPath: true
        , safeFileNames: false
        , preserveExtension: true
    }));

app.use('/', searchRouter);
app.use('/getResults', getResultsRouter);

app.get('/restart', function (req, res, next) {
    res.redirect("/");
});

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error', { title: 'Software Projekt WS20/21' , subtitle: 'Bilderweiterung mittels Methoden des maschinellen Lernens'});
});

hbs.registerPartials(__dirname + '/views/partials');
hbs.registerHelper('if_eq', function(a, b, opts) {
    if (a == true && b == true) {
        return opts.fn(this);
    } else {
        return opts.inverse(this);
    }
});

module.exports = app;
