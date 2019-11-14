
   var app = angular.module('myApp', []);
   app.controller('myController',
         function ($scope) {
            $scope.info = [0];
            $scope.add = function() {
                var timestamp = Date.parse(new Date());
                timestamp = timestamp / 1000;
                 $scope.info.push(timestamp);
                 $scope.$apply();
             };
    // 删除
            $scope.delete = function() {
                 $scope.info.pop();
                 $scope.$apply();
            };
        $scope.search=function(){
        var num=$scope.info.keys().length;
        var i=0;
         $scope.data='{"query": {"filtered": { "query": { "bool": {"'+$scope[i+'Cal']+'": {"match":{ "'+$scope[i+'Field']+'": "'+$scope[i+'Input']+'" }}';
         i=i+1;
        for(i; i=i+1; i<num){
            $scope.data=$scope.data+',"'+$scope[i+'Cal']+'": {"match":{ "'+$scope[i+'Field']+'": "'+$scope[i+'Input']+'" }}';
        }
        $scope.data=$scope.data+'}},"filter": {"range": {"year": {"gte": "'+$scope.time1+'","lte": "'+$scope.time2+'"},"price": {"gte": "'+$scope.price1+'","lte": "'+$scope.price2+'"},"doubanscore": {"gte": "'+$scope.score1+'","lte": "'+$scope.score2+'"},"page": {"gte": "'+$scope.page1+'","lte": "'+$scope.page2+'"}}}}}}';
             $http({
                method: 'POST',
                url: '../advancedSearch/',
                data: $scope.data
    }).then(function successCallback(response) {
//            $scope.names = response.data.sites;
        }, function errorCallback(response) {
            // 请求失败执行代码
    });

});
            });

