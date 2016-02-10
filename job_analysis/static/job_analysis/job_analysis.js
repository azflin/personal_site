function do_job_analysis(analysis_id){
    $('#results').empty();
    $('#results').append("<div>Gathering urls...</div>"
        + "<div id='urls'></div>"
        + "<div id='progress'></div>"
        + "<div style='display:inline-block;margin-right:20px;'><div id='word_frequency'>"
        + "</div></div>"
        + "<div style='display:inline-block;'><div id='bigram_frequency'>"
        + "</div></div>"
    );
    $.ajax({
        url : "/job_analysis/do_job_analysis/",
        type: "POST",
        data : {
            csrfmiddlewaretoken: CSRF_TOKEN,
            analysis_id: analysis_id,
            search_query: $('#id_search_query').val(),
            location: $('#id_location').val(),
            country: $('#id_country').val(),
            max_jobs: $('#id_max_jobs').val()
        },
    });
};


function poll_job_analysis(analysis_id) {
    setTimeout(function () {
        $.ajax({
            url: "/job_analysis/poll_job_analysis",
            type: "GET",
            data: {
                analysis_id: analysis_id
            },
            success: function (json) {
                if (json.frequencies) {
                    $('#progress').text("Scraped " + json.progress + " out of " + json.urls.length + " urls...");
                    $('#word_frequency').before('<div><b>Word Frequencies:</b></div>');
                    $('#bigram_frequency').before('<div><b>Bigram Frequencies:</b></div>');
                    var words_array = json.frequencies.words;
                    $.each(words_array, function (i, d) {
                        $('#word_frequency').append('<li>' + d[0] + ': ' + d[1] + '</li>');
                    });
                    var bigrams_array = json.frequencies.bigrams;
                    $.each(bigrams_array, function (i, d) {
                        $('#bigram_frequency').append('<li>' + d[0] + ': ' + d[1] + '</li>');
                    });
                }
                else if (json.progress) {
                    $('#progress').text("Scraped " + json.progress + " out of " + json.urls.length + " urls...");
                    poll_job_analysis(analysis_id);
                }
                else if (json.urls) {
                    console.log("got urls");
                    $('#urls').text("Found " + json.urls.length + " urls!");
                    poll_job_analysis(analysis_id);
                }
            }
        })
    }, 1000);
}

$(function(){

    var analysis_id = Math.floor((Math.random() * 1000000000) + 1);

    $('#post-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        do_job_analysis(analysis_id);
        poll_job_analysis(analysis_id);
    });
});