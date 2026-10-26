// ============================================================
// Locket Gold VIP - Ultimate Unlock
// Developer: LAMDev
// Website: https://dalymmo.com
// Channel: https://t.me/dalymmo
// ============================================================

const mapping = {
  'Locket': ['Gold']
};

var ua = $request.headers["User-Agent"] || $request.headers["user-agent"] || "",
    obj = JSON.parse($response.body);

obj.Attention = "Locket Gold VIP đã được kích hoạt thành công bởi LAMDev (dalymmo.com)!";

var lamdev = {
  auto_resume_date: null,
  display_name: "locket_1600_1y",
  is_sandbox: true,
  ownership_type: "PURCHASED",
  billing_issues_detected_at: null,
  management_url: "https://apps.apple.com/account/subscriptions",
  period_type: "normal",
  price: {
    "amount": 399000.0,
    "currency": "VND"
  },
  expires_date: "3000-04-21T00:00:00Z",
  grace_period_expires_date: null,
  refunded_at: null,
  unsubscribe_detected_at: null,
  original_purchase_date: "2006-04-21T00:00:00Z",
  purchase_date: "2026-04-21T00:00:00Z",
  store: "app_store",
  store_transaction_id: "2000001108724193"
};

var locketGold = {
  grace_period_expires_date: null,
  purchase_date: "2026-04-21T00:00:00Z",
  product_identifier: "locket_1600_1y",
  expires_date: "3000-04-21T00:00:00Z"
};

const match = Object.keys(mapping).find(e => ua.includes(e));

if (obj.subscriber) {
  obj.subscriber.subscriptions = obj.subscriber.subscriptions || {};
  obj.subscriber.entitlements = obj.subscriber.entitlements || {};

  if (match) {
    let [e, s] = mapping[match];
    if (s) {
      locketGold.product_identifier = s;
      obj.subscriber.subscriptions[s] = lamdev;
    } else {
      obj.subscriber.subscriptions["locket_1600_1y"] = lamdev;
    }
    obj.subscriber.entitlements[e] = locketGold;
  } else {
    obj.subscriber.subscriptions["locket_1600_1y"] = lamdev;
    obj.subscriber.entitlements.pro = locketGold;
    obj.subscriber.entitlements.Gold = locketGold;
  }
}

$done({
  body: JSON.stringify(obj)
});
