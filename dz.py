# Static Folder Name

dz_array = {
    "public": {
        "favicon": f"/images/favicon-16x16.png",
        "description": "Bank Movements: La PWA para analizar movimientos en tu banco",
        "og_title": "Bank Movements: La PWA para analizar movimientos en tu banco",
        "og_description": "Bank Movements: La PWA para analizar movimientos en tu banco",
        "title": "Bank Movements: La PWA para analizar movimientos en tu banco",
    },
    "global": {
        "css": [
            f"vendor/toastr/css/toastr.min.css",
            f"vendor/bootstrap-select/dist/css/bootstrap-select.min.css",
            f"css/style.css"
        ],
        "js": {
            "top": [
                f"vendor/global/global.min.js",
                f"vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
            ],
            "bottom": [
                f"js/custom.min.js",
                f"js/deznav-init.js",
            ]
        },

    },
    "pagelevel": {
        "app": {
            "app_views": {
                "css": {
                    "table_datatable_basic": [
                        f"vendor/datatables/css/jquery.dataTables.min.css",
                    ],
                    "page_login": [],
                    "page_register": [],
                    "page_forgot_password": [],
                    "page_lock_screen": [],
                    "page_error_400": [],
                    "page_error_403": [],
                    "page_error_404": [],
                    "page_error_500": [],
                    "page_error_503": [],
                },
                "js": {
                    "transactions": [
                        f"/vendor/chart.js/Chart.bundle.min.js",
                        f"/vendor/apexchart/apexchart.js",
                        f"/vendor/datatables/js/jquery.dataTables.min.js",
                        f"/js/plugins-init/datatables.init.js",
                    ],
                    "page_login": [],
                    "page_register": [],
                    "page_forgot_password": [],
                    "page_lock_screen": [],
                    "page_error_400": [],
                    "page_error_403": [],
                    "page_error_404": [],
                    "page_error_500": [],
                    "page_error_503": [],
                },
            }
        }
    }


}
