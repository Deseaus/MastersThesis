$( document ).ready(function() {

    // Area where files are uploaded to the server.
    // Server parses the img and returns a json result.
    // Once it is available, it is added to the remining panel.
    var mainDropzone = Dropzone.options.drop = {

        paramName: "file", // POST name for the file
        maxFilesize: 20, // MB
        autoProcessQueue: true,
        acceptedFiles: "image/*",
        init: function() {

            // Hide the text inside the dropzone when an upload begins
            this.on("addedfile", function(file) {

                $( "#droptext" ).hide();

            });

            // Once the image has been uploaded
            this.on("success", function(file, responseText) {

                this.removeFile(file); // Remove the img preview

                var template = $("#parsed-template").html();
                Mustache.parse(template);

                var data =
                {
                    "img-url": responseText.img_url,
                    "txt-url": responseText.txt_url,
                    "plain-txt": responseText.text,
                    "html-url": responseText.html_url,
                };

                var rendered = Mustache.render(template, data);
                $("#parsed-container").append(rendered);

            });

            // Inform the user and reset.
            this.on("error", function(file, message) {

                this.removeFile(file); // Remove the img preview

                // Render the template and add it to the DOM
                var template = $("#alert-template").html();
                Mustache.parse(template);
                var rendered = Mustache.render(template, {"message": message});
                $("#alert-container").append(rendered);

            });

            // Show the drop text again.
            this.on("queuecomplete", function(file, message) {

                $( "#droptext" ).fadeIn( 400 );

            });


            this.on('sending', function (file, xhr, formData){

                // Add the option selects to the formData
                formData.append('engine', $( "#engine" ).val());
                formData.append('parse-lang', $( "#parse-lang" ).val());
                formData.append('parse-font', $( "#parse-font" ).val());
                formData.append('post-processing', $( "#post-processing" ).val());

            });

        } // End init
    }; // End mainDropzone
}); // End jQuery