document.addEventListener('DOMContentLoaded', function () {
    let gridApi;

    // Define column definitions
    const columnDefs = [
        { headerName: "ID", field: "id", editable: false },
        { headerName: "Name", field: "name", editable: true },
        { headerName: "Category", field: "category", editable: true },
        { headerName: "Quantity", field: "quantity", editable: true },
        { headerName: "Price", field: "price", editable: true },
    ];

    // Define grid options
    const gridOptions = {
        columnDefs: columnDefs,
        rowData: null,
        onCellValueChanged: onCellValueChanged,
        onGridReady: function (params) {
            gridApi = params.api;
        }
    };

    // Initialize the grid
    const eGridDiv = document.querySelector("#myGrid");
    gridApi = agGrid.createGrid(eGridDiv, gridOptions);
    // new agGrid.Grid(eGridDiv, gridOptions);

    // WebSocket setup
    const socket = new WebSocket("ws://localhost:6789");

    socket.onopen = () => {
        console.log("WebSocket connection opened");
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (gridApi) {
            updateRowDataWithTotal(data);
        } else {
            console.error("Grid API is not initialized.");
        }
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
        console.log("WebSocket connection closed");
    };

    // Function to handle cell value changes
    function onCellValueChanged(event) {
        const updatedData = {
            id: event.data.id,
            name: event.data.name,
            category: event.data.category,
            quantity: event.data.quantity,
            price: event.data.price,
        };

        // Send updated data to the WebSocket server
        socket.send(JSON.stringify(updatedData));

        // Update the total in the footer
        updateRowDataWithTotal();
    }

    // Function to calculate the total price
    function calculateTotalPrice(rowData) {
        let totalPrice = 0;
        rowData.forEach(item => {
            totalPrice += parseFloat(item.price) || 0;
        });
        return totalPrice;
    }

    // Function to update row data with the total row
    function updateRowDataWithTotal(rowData = []) {
        const total = calculateTotalPrice(rowData);
        const totalRow = {
            id: '',
            name: 'Total',
            category: '',
            quantity: '',
            price: total
        };

        // Add the total row to the data
        const newData = [...rowData, totalRow];
        gridApi.setGridOption(newData); // Using setRowData after making sure gridApi is initialized
    }
});
