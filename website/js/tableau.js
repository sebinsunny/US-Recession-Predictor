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


initViz('graph1', 'https://public.tableau.com/views/FinalVisualisation_15899601798510/Dashboard5')
initViz('graph2', 'https://public.tableau.com/shared/GQ69JMJ9H?:display_count=y&:origin=viz_share_link')
initViz('graph3', 'https://public.tableau.com/views/houseprice_15911559588360/Dashboard1?:display_count=y&:origin=viz_share_link')

