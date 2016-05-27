"use strict";
main_app.controller("adminController", function($scope, $rootScope, $location) {
    $scope.mediaTree = {
        selected:{
            channel:null,
            mcc:null,
            account:null,
            campaign:null,
        },
        accordions:[{
            name: "channels",
            title: "Channel",
            status: {
                open: false
            }
        }, {
            name: "mccs",
            title: "MCC",
            status: {
                open: false
            }
        }, {
            name: "accounts",
            title: "Account",
            status: {
                open: false
            }
        }, {
            name: "campaigns",
            title: "Campaign",
            status: {
                open: false
            }
        }],
        data: {
            channels: [
                { name: "Google", entityId: "google" },
                { name: "Facebook", entityId: "facebook" }
            ],
            mccs:[
                { name: "All", parentId: "google", entityId: "m01"},
                { name: "All", parentId: "facebook", entityId: "m02" },
                { name: "Podium", parentId: "google", entityId: "m1" },
                { name: "Blik", parentId: "google", entityId: "m2" }
            ],
            accounts:[  { name: "TestAccount1",  parentId: "m01", entityId:"a1"},
                { name: "TestAccount2", parentId: "m01", entityId:"a2" },
                { name: "TestAccount3", parentId: "m1", entityId:"a3" },
                { name: "TestAccount31", parentId: "m1", entityId:"a4" },
                { name: "TestAccount4", parentId: "m2", entityId:"a5" },
                { name: "TestAccount44", parentId: "m2", entityId:"a6" }
            ],
            campaigns:[{ name: "TestCampaign1",  parentId:"a1", entityId:"c1"},
                { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"},
                { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"},
                { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"},
             { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"},
                { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"},
                { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"},
             { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"},
                { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"},
                { name: "TestCampaign2", parentId:"a2", entityId:"c2" },
                { name: "TestCampaign3", parentId:"a3", entityId:"c3" },
                { name: "TestCampaign4", parentId:"a4" , entityId:"c4"},
                { name: "TestCampaign5", parentId:"a5", entityId:"c5" },
                { name: "TestCampaign6", parentId:"a6" , entityId:"c6"},
                { name: "TestCampaign7",  parentId:"a1", entityId:"c7"},
                { name: "TestCampaign8", parentId:"a2", entityId:"c8" },
                { name: "TestCampaign9", parentId:"a3", entityId:"c9" },
                { name: "TestCampaign10", parentId:"a4" , entityId:"c10"},
                { name: "TestCampaign11", parentId:"a5", entityId:"c11" },
                { name: "TestCampaign12", parentId:"a6" , entityId:"c12"}]
        }

    };
    $scope.getMediaFilter = function (parentName) {
        var media = null;
        switch (parentName){
            case "channels":
                media = $scope.mediaTree.selected.channel;
                break;
            case "mccs":
                media = $scope.mediaTree.selected.mcc;
                break;
            case "accounts":
                media = $scope.mediaTree.selected.account;
                break;
        }
        if(media){
            return {parentId: media.entityId};
        }
        return null;
    };
    $scope.getAccordionTitle = function (accordion) {
        if(!accordion) return "No Title";
        var media = null;
        switch (accordion.name){
            case "channels":
                media = $scope.mediaTree.selected.channel;
                break;
            case "mccs":
                media = $scope.mediaTree.selected.mcc;
                break;
            case "accounts":
                media = $scope.mediaTree.selected.account;
                break;
             case "campaigns":
                media = $scope.mediaTree.selected.campaign;
                break;
        }
        if(media){
            return  media.name + ' (' + accordion.title + ')';
        }
        return accordion.title;
    };
    $scope.changeEntity = function (accordion, media) {
        if(!accordion || !media) return;
         switch (accordion.name){
            case "channels":
                $scope.mediaTree.selected.channel = media;
                break;
            case "mccs":
                $scope.mediaTree.selected.mcc = media;
                break;
            case "accounts":
                $scope.mediaTree.selected.account = media;
                break;
             case "campaigns":
                $scope.mediaTree.selected.campaign= media;
                break;
        }
        accordion.status.open = false;
    };
});
