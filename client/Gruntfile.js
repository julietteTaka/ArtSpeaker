module.exports = function(grunt) //à toujours écrire
{

  // Project configuration.
  grunt.initConfig(
  {
    less : 
    {
      dev : 
      {
        files : 
        {
          '.tmp/styles/main.css' : 'static/styles/main.less'
          //target, 
        }
      }
    },

    autoprefixer : 
    {
      dev : 
      {
        files : 
        {
          '.tmp/styles/main.css' : '.tmp/styles/main.css'
        }
      }
    },

    watch :{
      //target, ce que l'on regarde :
      less : {
        files : ['static/styles/*.less'],
        tasks : ['css']
      },
      livereload : {
        files : ['.tmp/styles/main.css', 'static/index.html'],
        options : {
          livereload : true
        }
      }
    },

    connect : {
      server : {
        options : {
          base : ['static', '.tmp'],
          livereload : true,
          open : true,
          hostname : 'localhost'
        }
      }
    },

    clean : {
      dev : ['.tmp']
    }

  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-autoprefixer');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-clean');

  grunt.registerTask('server', ['clean', 'css', 'connect', 'watch']);
  grunt.registerTask('css', ['less', 'autoprefixer']);


  // Default task(s).
  grunt.registerTask('default', []);

};