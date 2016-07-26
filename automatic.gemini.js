/*

************************
*** config file help ***
************************

containers: this section refers to the number of ad templates to be included for this partner. each javascript object refers to a seperate template. the same template can be include multiple times.

target: this refers to the parent container for the ad to be sent to. when assigning this section, you should aim to get your selector as close as you can to the desired location for the ad.

selector: this is the element that gemini will try to match against within the target container. these should be direct child of the target container.

template: refers to the HTML snippet that is assigned / associated with this particular placement. the template path provided here will be inserted into the taget container and repeated x number of times after the first position set. templates can be shared across multiple placements.

first: represents the initial position within the target that ads will commence.

interval: this is the index that tells gemini when the next ad unit should occur within the target container. this index pattern is counted after the first ad position and will occur until no more ads are available to be served.

************************
******* end help *******
************************

*/


(function () {
    new GeminiNative({
        containers: [
            {
                target: ".example.class",
                selector: "div",
                template: "automatic/modulename/modulename",
                frequency: {
                    first: 1,
                    interval: 2
                }
            }
        ],
        syndication: {
            section: "1234567"
        }
    });
})();