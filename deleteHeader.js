/***********************************************
> deleteHeader by LAMDev - dalymmo.com
***********************************************/

function setHeaderValue(e, a, d) {
  var r = a.toLowerCase();
  r in e ? (e[r] = d) : (e[a] = d);
}

var modifiedHeaders = ($request && $request.headers) ? $request.headers : {};
setHeaderValue(modifiedHeaders, "X-RevenueCat-ETag", "");
setHeaderValue(modifiedHeaders, "x-revenuecat-etag", "");
setHeaderValue(modifiedHeaders, "If-None-Match", "");
setHeaderValue(modifiedHeaders, "if-none-match", "");

delete modifiedHeaders["X-RevenueCat-ETag"];
delete modifiedHeaders["x-revenuecat-etag"];
delete modifiedHeaders["If-None-Match"];
delete modifiedHeaders["if-none-match"];

$done({ headers: modifiedHeaders });
