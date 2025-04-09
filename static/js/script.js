

	let currentForm=null;

    var a='';

	
	function closeReceipt() {
        hideElements("hide");
    }
	
    function openForm(formId) {
        hideElements("hide");
	    closeReceipt()
        if (currentForm) { document.getElementById(currentForm).style.display = 'none';}
        document.getElementById(formId).style.display = 'block';
        currentForm = formId;
        const form = document.getElementById(formId + 'Fields');
        if (form) {form.reset(); }// Reset all form fields to default values
        const submissionSummary = document.getElementById('submission-summary');
        if(formId=='form1'){
            document.getElementById('endOffSet').ariaReadOnly=true;
        }
        if (submissionSummary) {submissionSummary.style.display = 'none';
        }
	}
    
    document.addEventListener("DOMContentLoaded", function () {
        const openChatLink = document.getElementById("open-chat");
        const chatContainer = document.getElementById("chat-container");
        const closeChat = document.getElementById("close-chat");
        const sendMessageBtn = document.getElementById("send-message");
        const chatInput = document.getElementById("chat-input");
        const chatBody = document.getElementById("chat-body");
       
        const topicButtons= document.getElementsByClassName("seg-btn");



        for (i = 0; i < topicButtons.length; ++i) {
            topicButtons[i].addEventListener("click",function(e){
                document.querySelector(".seg-btn.selectedOption").classList.remove("selectedOption");
                e.target.classList.add("selectedOption")
                a=e.currentTarget.dataset.value
                console.log(e.currentTarget.dataset.value)
            })
          };
        
        // Open chatbot when clicking the sidebar link
        openChatLink.addEventListener("click", function (event) {
            event.preventDefault();
            hideElements("hide");
            chatContainer.style.display = "flex";
            
        
        });
    
        // Close chatbot
        closeChat.addEventListener("click", function () {
            chatContainer.style.display = "none";
        });
    
        // Function to send messages
    function sendMessage() {
            let userText = chatInput.value.trim();
            if (userText === "") return;
    
            // Create user message
            let userMessage = document.createElement("div");
            userMessage.classList.add("user-message");
            userMessage.textContent = userText;
            chatBody.appendChild(userMessage);
    
            // Auto-scroll to latest message
            chatBody.scrollTop = chatBody.scrollHeight;
    
            // Clear input field
            chatInput.value = "";
            const get_chat_data = '/get_chat_data'+a+'/'
            userMessage={"message": userText}
            const jsonData1=JSON.stringify(userMessage);
            console.log(JSON.stringify(userMessage));
            const csrftoken = getCookie('csrftoken');
            fetch(get_chat_data, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') 
                },
                body: jsonData1,
                credentials: "same-origin"
            })
            .then((response) => response.json())
            .then((data) =>{
                let botMessage = document.createElement("div");
                botMessage.classList.add("bot-message");
                botMessage.textContent = data.response;
                chatBody.appendChild(botMessage);
                chatBody.scrollTop = chatBody.scrollHeight;


            } )
            .catch(error => console.error(error));

    
            // // Simulate bot response
            // setTimeout(() => {
            //     let botMessage = document.createElement("div");
            //     botMessage.classList.add("bot-message");
            //     botMessage.textContent = "I'm here to help! 😊";
            //     chatBody.appendChild(botMessage);
    
            //     // Auto-scroll
            //     chatBody.scrollTop = chatBody.scrollHeight;
            // }, 1000);
        }
    
        // Send message on button click
        sendMessageBtn.addEventListener("click", sendMessage);
    
        // Send message on Enter key
        chatInput.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                
             
                sendMessage();
            }
        });
    });

    function appendMessage(text, className) {
        const messageElement = document.createElement("div");
        messageElement.classList.add(className);
        messageElement.textContent = text;
        chatBody.appendChild(messageElement);
        chatBody.scrollTop = chatBody.scrollHeight;
        
         }
        function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        // Display User Message
        appendMessage(message, "user-message");

        // Clear Input
        userInput.value = "";

        // Simulate Bot Typing
        setTimeout(() => {
            appendMessage("Let me check that for you... 🤖", "bot-message");

            setTimeout(() => {
                appendMessage("Here's the information you need! 🚀", "bot-message");
            }, 2000);
        }, 1000);
    }

  

   

    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }

    // function showRequestData2() {
    //     hideElements("hide");
    //     document.getElementById('requestTable').style.display = 'block';
    //     $('#requestDataTable').DataTable({
    //         dom: 'Bfrtip',
    //         buttons: [
    //             { extend: 'excelHtml5', text: 'ExportExcel', className: 'btn-export btn-excel' }
    //         ],
    //         // Other DataTables options...
    //       });
    //     }
    function showRequestData2() {
        hideElements("hide");
        document.getElementById('requestTable').style.display = 'block';
        $.ajax({
            url: "/get_recon_result/",
            type: "GET",
            success: function (response) {
                let tableBody = $("#requestDataTable tbody");
                tableBody.empty();
                
                response.forEach(ReconResult => {
                    let row = `<tr>
s                       <td>${ReconResult.RequestID}</td>
                        <td>${ReconResult.JoinKey}</td>
                        <td>${ReconResult.FieldName}</td>
                        <td>${ReconResult.Kafka}</td>
                        <td>${ReconResult.Impala}</td>
                        <td>${ReconResult.Gemfire}</td>
                        <td>${ReconResult.ReconStatus}</td>
                        <td>${ReconResult.env}</td>
                    </tr>`;
                    tableBody.append(row);
                });

                // Destroy existing DataTable instance before re-initializing
                if ($.fn.DataTable.isDataTable("#requestDataTable")) {
                    $("#requestDataTable").DataTable().destroy();
                }

                // Initialize DataTable with sorting, filtering, pagination & export
                $("#requestDataTable").DataTable({
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'ExportExcel', className: 'btn-export btn-excel' }
                    ],
                    paging: true,      // Enable pagination
                    searching: true,   // Enable search filter
                    ordering: true,    // Enable sorting
                    responsive: true,  // Enable responsive design
                });
            },
            error: function () {
                alert("Error fetching data!");
            }
        });
    }




   $(document).ready(function () {
    $("#loadHistory").click(function (event) {
        event.preventDefault();
        hideElements("hide");
        
        // Hide other sections
        // $("#form1,#form2,#form3,#form4,#form5,#form6,#countrecon,#skrecon,#chat-container, #chartContainer, #requestTable1, #requestTable, #receipt, #form1 ,#gzrecon,#jobsrecon").hide();
        $("#requestTable2").show(); // Show the table
        
        $.ajax({
            url: "/get_recon_data/",
            type: "GET",
            success: function (response) {
                let tableBody = $("#requestDataTable2 tbody");
                tableBody.empty();
                
                response.forEach(ReconVO => {
                    let row = `<tr>
                        <td><a href="#" onclick="showRequestData2()">${ReconVO.reqId}</a></td>
                        <td>${ReconVO.name}</td>
                        <td>${ReconVO.created}</td>
                        <td>${ReconVO.tblName}</td>
                        <td>${ReconVO.pipeline}</td>
                        <td>${ReconVO.temporal}</td>
                        <td>${ReconVO.onBoarding}</td>
                        <td>${ReconVO.batch}</td>
                        <td>${ReconVO.env}</td>
                        <td>${ReconVO.field6}</td>
                    </tr>`;
                    tableBody.append(row);
                });

                // Destroy existing DataTable instance before re-initializing
                if ($.fn.DataTable.isDataTable("#requestDataTable2")) {
                    $("#requestDataTable2").DataTable().destroy();
                }

                // Initialize DataTable with sorting, filtering, pagination & export
                $("#requestDataTable2").DataTable({
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'ExportExcel', className: 'btn-export btn-excel' }
                    ],
                    paging: true,      // Enable pagination
                    searching: true,   // Enable search filter
                    ordering: true,    // Enable sorting
                    responsive: true,  // Enable responsive design
                });
            },
            error: function () {
                alert("Error fetching data!");
            }
        });
    });
});



$(document).ready(function () {
    $("#loadskrecon").click(function (event) {
        event.preventDefault();
        hideElements("hide");
        // Hide other sections
       //  $("#form1,#form2,#form3,#form4,#form5,#countrecon,#chat-container, #gzrecon,#jobsrecon,#chartContainer, #requestTable1, #requestTable, #receipt, #form1,#requestTable2",).hide();
        $("#skrecon").show(); // Show the table
        
        $.ajax({
            url: "/get_skrecon_data/",
            type: "GET",
            success: function (response) {
                let tableBody = $("#skDatarecon tbody");
                tableBody.empty();
                
                response.forEach(SKReconTable => {
                    let row = `<tr>
                        <td>${SKReconTable.tblname}</td>    
                        <td>${SKReconTable.name}</td>
                        <td>${SKReconTable.mismatchFreq}</td>
                        <td>${SKReconTable.mismatchCount}</td>
                        <td>${SKReconTable.created}</td>
                         <td>${SKReconTable.env}</td>
                         </tr>`;
                    tableBody.append(row);
                });

                // Destroy existing DataTable instance before re-initializing
                if ($.fn.DataTable.isDataTable("#skDatarecon")) {
                    $("#skDatarecon").DataTable().destroy();
                }

                // Initialize DataTable with sorting, filtering, pagination & export
                $("#skDatarecon").DataTable({
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'ExportExcel', className: 'btn-export btn-excel' }
                    ],
                    paging: true,      // Enable pagination
                    searching: true,   // Enable search filter
                    ordering: true,    // Enable sorting
                    responsive: true,  // Enable responsive design
                });
            },
            error: function () {
                alert("Error fetching data!");
            }
        });
    });
});



$(document).ready(function () {
    $("#loadcountrecon").click(function (event) {
        event.preventDefault();
        hideElements("hide");
        // Hide other sections
       //  $("#chat-container, #gzrecon,#jobsrecon,#chartContainer, #requestTable1, #requestTable, #receipt,#form1,#form2,#form3,#form4,#form5,#skrecon,#requestTable2",).hide();
        $("#countrecon").show(); // Show the table
        
        $.ajax({
            url: "/get_regioncount_data/",
            type: "GET",
            success: function (response) {
                let tableBody = $("#countDatarecon tbody");
                tableBody.empty();
                
                response.forEach(GemfireCountTable1 => {
                    let row = `<tr>
                     <td>${GemfireCountTable1.tblName}</td>   
                    <td>${GemfireCountTable1.name}</td>
                        <td>${GemfireCountTable1.countDiff}</td>
                        <td>${GemfireCountTable1.hiveCount}</td>
                         <td>${GemfireCountTable1.gemfireCount}</td>
                        <td>${GemfireCountTable1.created}</td>
                         <td>${GemfireCountTable1.env}</td>
                         </tr>`;
                    tableBody.append(row);
                });

                // Destroy existing DataTable instance before re-initializing
                if ($.fn.DataTable.isDataTable("#countDatarecon")) {
                    $("#countDatarecon").DataTable().destroy();
                }

                // Initialize DataTable with sorting, filtering, pagination & export
                $("#countDatarecon").DataTable({
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'ExportExcel', className: 'btn-export btn-excel' }
                    ],
                    paging: true,      // Enable pagination
                    searching: true,   // Enable search filter
                    ordering: true,    // Enable sorting
                    responsive: true,  // Enable responsive design
                });
            },
            error: function () {
                alert("Error fetching data!");
            }
        });
    });
});



$(document).ready(function () {
    $("#loadgzrecon").click(function (event) {
        event.preventDefault();
        hideElements("hide");
        // Hide other sections
       //  $("#chat-container,#form1,#form2,#form3,#form4,#form5,#jobsrecon, #chartContainer, #requestTable1, #requestTable, #receipt, #form1,#skrecon,#requestTable2",).hide();
        $("#gzrecon").show(); // Show the table
        
        $.ajax({
            url: "/get_gz_data/",
            type: "GET",
            success: function (response) {
                let tableBody = $("#gzDatarecon tbody");
                tableBody.empty();
                
                response.forEach(GZTable => {
                    let row = `<tr>
                         <td>${GZTable.name}</td>
                         <td>${GZTable.statts}</td>
                         <td>${GZTable.endts}</td>
                        <td>${GZTable.env}</td>
                        <td>${GZTable.eapps}</td>
                        <td>${GZTable.ps}</td>
                         <td>${GZTable.pltps}</td>
                         </tr>`;
                    tableBody.append(row);
                });

                // Destroy existing DataTable instance before re-initializing
                if ($.fn.DataTable.isDataTable("#gzDatarecon")) {
                    $("#gzDatarecon").DataTable().destroy();
                }

                // Initialize DataTable with sorting, filtering, pagination & export
                $("#gzDatarecon").DataTable({
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'ExportExcel', className: 'btn-export btn-excel' }
                    ],
                    paging: true,      // Enable pagination
                    searching: true,   // Enable search filter
                    ordering: true,    // Enable sorting
                    responsive: true,  // Enable responsive design
                });
            },
            error: function () {
                alert("Error fetching data!");
            }
        });
    });
});




$(document).ready(function () {
    $("#loadjobs").click(function (event) {
        event.preventDefault();
        hideElements("hide");
        // Hide other sections
       //  $("#gzrecon,#chat-container, #chartContainer, #requestTable1, #form1,#form2,#form3,#form4,#form5,#requestTable, #receipt, #form1,#skrecon,#requestTable2",).hide();
        $("#jobsrecon").show(); // Show the table
        
        $.ajax({
            url: "/get_jobs_data/",
            type: "GET",
            success: function (response) {
                let tableBody = $("#jobsDatarecon tbody");
                tableBody.empty();
                
                response.forEach(Jobs => {
                    let row = `<tr>
                         <td>${Jobs.table}</td>
                         <td>${Jobs.type}</td>
                         <td>${Jobs.jobName}</td>
                         <td>${Jobs.POC}</td>
                         <td>${Jobs.onBoarding}</td>
                         <td>${Jobs.env}</td>
                         <td>${Jobs.lastts}</td>
                         <td>${Jobs.executionTime}</td>
                         </tr>`;
                    tableBody.append(row);
                });


              
                






                // Destroy existing DataTable instance before re-initializing
                if ($.fn.DataTable.isDataTable("#jobsDatarecon")) {
                    $("#jobsDatarecon").DataTable().destroy();
                }

                // Initialize DataTable with sorting, filtering, pagination & export
                $("#jobsDatarecon").DataTable({
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'ExportExcel', className: 'btn-export btn-excel' }
                    ],
                    paging: true,      // Enable pagination
                    searching: true,   // Enable search filter
                    ordering: true,    // Enable sorting
                    responsive: true,  // Enable responsive design
                });
            },
            error: function () {
                alert("Error fetching data!");
            }
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('formId1');
    const confirmationMessageElement = document.getElementById('confirmation-message');
    const submitBtn = document.getElementById('bt1');
    var requestId = "Req" + new Date().toISOString().slice(0, 10).replace(/-/g, "") + Date.now().toString().slice(-4);
    submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            hideElements("hide");
            const formData = new FormData(form);
            formData.append("reqId", requestId);
            formData.append("name", "Admin");
            formData.append("date",  "2025-04-02");
            formData.append("created", "2025-04-02" );
            const jsonData = Object.fromEntries(formData.entries());
            console.log(jsonData);
            const jsonData1=JSON.stringify(jsonData);
            console.log(JSON.stringify(jsonData));
            const saveUserDataUrl = '/save_recon_data/';
            const csrftoken = getCookie('csrftoken');
            fetch(saveUserDataUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: jsonData1
            })
            .then((response) => response.json())
            .then((data) => console.log(data))
            .catch(error => console.error(error));
            document.getElementById('receipt').style.display = 'block';
            document.getElementById('form1').style.display = 'none';
            document.getElementById('requestId').innerText = requestId;
    });
})



document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('formId2');
    const submitBtn = document.getElementById('bt2');
    submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            hideElements("hide");
            const jsonData=JSON.stringify( Object.fromEntries(new FormData(form).entries()));
            const saveUserDataUrl = '/get_skrecon_data/';
            const csrftoken = getCookie('csrftoken');
            fetch(saveUserDataUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: jsonData
            })
            .then((response) => response.json())
            .then((data) => console.log(data))
            .catch(error => console.error(error));
            const jsonString = '{"name":"John","age":30,"city":"New York"}';
            document.getElementById('output2').value = JSON.stringify(JSON.parse(jsonString), null, 4);
            document.getElementById('form2').style.display = 'block';
 });
})


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('formId3');
    const submitBtn = document.getElementById('bt3');
    submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            hideElements("hide");
            const jsonData=JSON.stringify( Object.fromEntries(new FormData(form).entries()));
            const saveUserDataUrl = '/get_skrecon_data/';
            const csrftoken = getCookie('csrftoken');
            fetch(saveUserDataUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: jsonData
            })
            .then((response) => response.json())
            .then((data) => console.log(data))
            .catch(error => console.error(error));
            const jsonString = '{"name":"John","age":30,"city":"New York"}';
            document.getElementById('output3').value = JSON.stringify(JSON.parse(jsonString), null, 4);
            document.getElementById('form3').style.display = 'block';
 });
})


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('formId4');
    const submitBtn = document.getElementById('bt4');
    submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            hideElements("hide");
            const jsonData=JSON.stringify( Object.fromEntries(new FormData(form).entries()));
            const saveUserDataUrl = '/get_skrecon_data/';
            const csrftoken = getCookie('csrftoken');
            fetch(saveUserDataUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: jsonData
            })
            .then((response) => response.json())
            .then((data) => console.log(data))
            .catch(error => console.error(error));
            const jsonString = '{"name":"John","age":30,"city":"New York"}';
            document.getElementById('output4').value = JSON.stringify(JSON.parse(jsonString), null, 4);
            document.getElementById('form4').style.display = 'block';
 });
})


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('formId5');
    const submitBtn = document.getElementById('bt5');
    submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            hideElements("hide");
            const jsonData=JSON.stringify( Object.fromEntries(new FormData(form).entries()));
            const saveUserDataUrl = '/get_skrecon_data/';
            const csrftoken = getCookie('csrftoken');
            fetch(saveUserDataUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: jsonData
            })
            .then((response) => response.json())
            .then((data) => console.log(data))
            .catch(error => console.error(error));
            const jsonString = '{"name":"John","age":30,"city":"New York"}';
            document.getElementById('output5').value = JSON.stringify(JSON.parse(jsonString), null, 4);
            document.getElementById('form5').style.display = 'block';
 });
})



document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('formId6');
    const submitBtn = document.getElementById('bt6');
    submitBtn.addEventListener('click', (e) => {
            hideElements("hide");
            e.preventDefault();
            const jsonData=JSON.stringify( Object.fromEntries(new FormData(form).entries()));
            const saveUserDataUrl = '/get_skrecon_data/';
            const csrftoken = getCookie('csrftoken');
            fetch(saveUserDataUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: jsonData
            })
            .then((response) => response.json())
            .then((data) => console.log(data))
            .catch(error => console.error(error));
            const jsonString = '{"name":"John","age":30,"city":"New York"}';
            document.getElementById('output6').value = JSON.stringify(JSON.parse(jsonString), null, 4);
            document.getElementById('form6').style.display = 'block';
 });
})




document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('formId7');
    const submitBtn = document.getElementById('bt7');
    submitBtn.addEventListener('click', (e) => {
            hideElements("hide");
            e.preventDefault();
            const jsonData=JSON.stringify( Object.fromEntries(new FormData(form).entries()));
            const saveUserDataUrl = '/get_skrecon_data/';
            const csrftoken = getCookie('csrftoken');
            fetch(saveUserDataUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: jsonData
            })
            .then((response) => response.json())
            .then((data) => console.log(data))
            .catch(error => console.error(error));
            const jsonString = '{"name":"John","age":30,"city":"New York"}';
            document.getElementById('output7').value = JSON.stringify(JSON.parse(jsonString), null, 4);
            document.getElementById('form7').style.display = 'block';
 });
})

function showElements(classNames) {
    if (!Array.isArray(classNames)) {
        classNames = [classNames]; // Convert to array if a single class is given
    }

    classNames.forEach(className => {
        document.querySelectorAll(`.${className}`).forEach(element => {
            element.style.display = ""; // Show elements (default display)
        });
    });
}

function hideElements(classNames) {
   
    if (!Array.isArray(classNames)) {
        classNames = [classNames]; // Convert to array if a single class is given
    }

    classNames.forEach(className => {
        document.querySelectorAll(`.${className}`).forEach(element => {
            element.style.display = "none"; // Hide elements
        });
    });
}



document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("showChart")?.addEventListener("click", function() {
        document.getElementById("chartContainer").style.display = "block";  // Show the chart container

        // Fetch data for each chart
        const chartUrls = [
            // 'http://localhost:8000/chart1/',  // Chart 1 endpoint
            // 'http://localhost:8000/chart2/',
            // 'http://localhost:8000/chart3/',  // Chart 1 endpoint
            // 'http://localhost:8000/chart4/',
            // 'http://localhost:8000/chart5/',  // Chart 1 endpoint
            // 'http://localhost:8000/chart6/',
            // 'http://localhost:8000/chart7/',  // Chart 1 endpoint
            // 'http://localhost:8000/chart8/',

            '/chart1/',  // Chart 1 endpoint
            '/chart2/',
            '/chart3/',  // Chart 1 endpoint
            '/chart4/',
            '/chart5/',  // Chart 1 endpoint
            '/chart6/',
            '/chart7/',  // Chart 1 endpoint
            '/chart8/',
        ];

        // Fetch data for each chart
        Promise.all(chartUrls.map(url => fetch(url).then(response => response.json())))
            .then(dataArray => {
                // Loop through each chart and render
                dataArray.forEach((data, index) => {
                    // Call renderChart function for each chart
                    renderChart(`chart${index + 1}`, data);
                });
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
            });
    });
});

function renderChart(chartId, chartData) {
    let options = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                top: 20,
                left: 10,
                right: 10,
                bottom: 10
            }
        },
        plugins: {
            datalabels: {
                anchor: 'end',
                align: 'top',
                font: {
                    weight: 'bold',
                    size: 14
                },
                color: 'black',
                formatter: function(value) {
                    return value / 1000 + 'K';  // Format the value as 'K'
                }
            }
        },
        scales: {
            y: {
                ticks: {
                    callback: function(value) {
                        if (value >= 1000) {
                            return value / 1000 + 'K';  // Format the y-axis as 'K'
                        }
                        return value;
                    }
                }
            }
        }
    };
    
    Chart.register(ChartDataLabels);
    // Create the chart using the passed data and chartId
    new Chart(document.getElementById(chartId), {
        type: "bar",  // Type of chart (bar)
        data: {
            labels: chartData.labels,  // Use the labels from the API
            datasets: [{
                data: chartData.datasets[0].data,  // Use the data from the API
                backgroundColor: ["#007bff", "#28a745", "#ffc107"], // Add colors as needed
                borderColor: "#fff",
                borderWidth: 1
            }]
        },
        options: options  // Chart options with data labels and formatted y-axis
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');

    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('hidden');
      content.classList.toggle('sidebar-hidden');
    });
});