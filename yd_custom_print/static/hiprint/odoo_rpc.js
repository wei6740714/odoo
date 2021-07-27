
function _genericJsonRpc (fct_name, params, fct) {
    var deferred = $.Deferred();
    var data = {
        jsonrpc: "2.0",
        method: fct_name,
        params: params,
        id: Math.floor(Math.random() * 1000 * 1000 * 1000)
    };

    var xhr = fct(data);
    var result = xhr.pipe(function(result) {
        if (result.error !== undefined) {
            if (result.error.data.arguments[0] !== "bus.Bus not available in test mode") {
                var func = console.error.bind(console);
                if (result.error.data.exception_type === "user_error") {
                    func = console.log.bind(console);
                }
                func(
                    "Server application error\n",
                    "Error code:", result.error.code, "\n",
                    "Error message:", result.error.message, "\n",
                    "Error data message:\n", result.error.data.message, "\n",
                    "Error data debug:\n", result.error.data.debug
                );
            }
            return $.Deferred().reject("server", result.error);
        } else {
            return result.result;
        }
    }, function() {
        var def = $.Deferred();
        return def.reject.apply(def);
    });

    result.then(function (result) {
        deferred.resolve(result);
    });
    return deferred;
}

function _jsonRpc(url, fct_name, params) {
    return _genericJsonRpc(fct_name, params, function(data) {
        return $.ajax(url, {
            url: url,
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify(data, Date.parse(new Date())),
            contentType: 'application/json'
        });
    });
}

function odoo_rpc(params) {
    var def=_jsonRpc('/web/dataset/call_kw', 'call', params)
    return def
}





