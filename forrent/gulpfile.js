var gulp = require('gulp');
var browserSync = require('browser-sync').create();
var notify = require('gulp-notify');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var cssnano = require('gulp-cssnano');
var browserify = require('browserify');
var tap = require('gulp-tap');
var buffer = require('gulp-buffer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var imagemin = require('gulp-imagemin');
var wait = require('gulp-wait');

var project = "forrent/";
var src = "src/";
var dest = project + "static/";

var htmlFiles = ["**/templates/**/*.html"];
var scssFiles = ["**/" + src + "scss/**/*.scss"];
var jsFiles = ["**/" + src + "js/**/*.js"];
var imagesDir = [project + src + "img/*"];
var fontsDir = [project + src + "fonts/*"];

var backendFiles = ["**/*.py"];

gulp.task(
    "default",
    ["compile-sass", "concat-js", "optimize-images", "copy-fonts"],
    function () {

        browserSync.init({
            proxy: "localhost:8000"

        });

        gulp.watch(htmlFiles, ["updated-html"]);

        gulp.watch(scssFiles, ["compile-sass"]);

        gulp.watch(jsFiles, ["concat-js"]);

        gulp.watch(imagesDir, ["optimize-images"]);

        gulp.watch(fontsDir, ["copy-fonts"]);

        gulp.watch(backendFiles, ["updated-backend"]);

    });

gulp.task("updated-html", function () {
    gulp.src("./")
        .pipe(browserSync.stream())
        .pipe(notify({
            title: "HTML",
            message: "Updated"
        }));
});

gulp.task("compile-sass", function () {
    gulp.src("./" + project + src + "scss/style.scss")
        .pipe(sourcemaps.init())
        .pipe(sass()
            .on('error', sass.logError)
            .on('error', notify.onError({
                title: "SASS",
                message: "Error"
            })))
        .pipe(autoprefixer())
        .pipe(cssnano())
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest(dest + "css"))
        .pipe(browserSync.stream())
        .pipe(notify({
            title: "SASS",
            message: "Compiled"
        }));
});

gulp.task("concat-js", function () {
    gulp.src("./" + project + src + "js/app.js")
        .pipe(sourcemaps.init())
        .pipe(tap(function (file) {
            file.contents = browserify(file.path).bundle();
        }))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest(dest + "js"))
        .pipe(browserSync.stream())
        .pipe(notify({
            title: "JS",
            message: "Concatenated"
        }));
});

gulp.task("optimize-images", function () {
    gulp.src(imagesDir)
        .pipe(imagemin())
        .pipe(gulp.dest(dest + "img"))
        .pipe(browserSync.stream())
        .pipe(notify({
            title: "Images",
            message: "Optimized"
        }));
});

gulp.task("copy-fonts", function () {
    gulp.src(fontsDir)
        .pipe(gulp.dest(dest + "fonts"))
        .pipe(browserSync.stream())
        .pipe(notify({
            title: "Fonts",
            message: "Copied"
        }));
});

gulp.task("updated-backend", function () {
    gulp.src("./")
        .pipe(wait(3000))
        .pipe(browserSync.stream())
        .pipe(notify({
            title: "Backend",
            message: "Updated"
        }));
});


