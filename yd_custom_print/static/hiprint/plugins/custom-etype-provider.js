var customElementTypeProvider = (function () {
    return function (options) {

        var addElementTypes = function (context) {
            context.addPrintElementTypes(
                "testModule",
                [
                    new hiprint.PrintElementTypeGroup("常规", [
                        { tid: 'testModule.text', title: '文本', data: '测试文本', type: 'text' },
                        { tid: 'testModule.image', title: '图片', data: 'css/image/hi.png', type: 'image' },
                        { tid: 'testModule.longText', title: '长文', data: '155123456789', type: 'longText' },
                        {
                            tid: 'testModule.tableCustom',
                            title: '表格',
                            type: 'tableCustom'
                        },
                        {
                            tid: 'testModule.html', title: 'html',
                            formatter: function (data, options) {
                                return $('<div style="height:100%;width:100%;background:red;border-radius: 50%;"></div>');
                            },
                            type: 'html'
                        },
                        { tid: 'testModule.customText', title: '自定义文本', customText: '自定义文本', custom: true, type: 'text' }
                    ]),
                    new hiprint.PrintElementTypeGroup("辅助", [
                        {
                            tid: 'testModule.hline',
                            title: '横线',
                            type: 'hline'
                        },
                        {
                            tid: 'testModule.vline',
                            title: '竖线',
                            type: 'vline'
                        },
                        {
                            tid: 'testModule.rect',
                            title: '矩形',
                            type: 'rect'
                        },
                        {
                            tid: 'testModule.oval',
                            title: '椭圆',
                            type: 'oval'
                        },
                    ])
                ]
            );
        };

        return {
            addElementTypes: addElementTypes
        };

    };
})();