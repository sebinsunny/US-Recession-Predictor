function initViz(id, url) {
    var containerDiv = document.getElementById(id),
        url = url,
        options = {


            width: "1100px",
            height: "600px",
            hideTabs: true,
            onFirstInteractive: function () {
                console.log("Run this code when the viz has finished loading.");

            }
        };

    var viz = new tableau.Viz(containerDiv, url, options);

    // Create a viz object and embed it in the container div.
}




