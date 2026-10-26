/***********************************************
> deleteHeader by LAMDev - dalymmo.com
***********************************************/

function setHeaderValue(e, a, d) {
  var r = a.toLowerCase();
  r in e ? (e[r] = d) : (e[a] = d);
}

var modifiedHeaders = $request.headers;
setHeaderValue(modifiedHeaders, "X-RevenueCat-ETag", "");
setHeaderValue(modifiedHeaders, "x-revenuecat-etag", "");
$done({ headers: modifiedHeaders });
