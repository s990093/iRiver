let data
function submitForm() {
  const query = document.getElementById("query").value
  const loading = document.getElementById("loading");
  const table_title = document.getElementById("table_title");
  const tableBody = document.getElementById("table-body");
  loading.style.display = "block";
  table_title.style.display = "none";
  //清空
   tableBody.innerHTML = "";
  fetch(`/crawl?text=${query}`)
    .then(response => response.json())
    .then(data => {
      data.videos.forEach(video => {
        const tr = document.createElement("tr");
        const td1 = document.createElement("td");
        const td2 = document.createElement("td");
        const td3 = document.createElement("td");
        const td4 = document.createElement("td");
        const img = document.createElement("img");
        const a = document.createElement("a");
        const author = document.createElement("span");
        const authorImg = document.createElement("img");

        img.src = video.img || "https://via.placeholder.com/720x405.png?text=No+Image";
        img.alt = "none";
        img.width = "50";
        a.href = "#";
        a.dataset.url = video.url;
        a.textContent = video.title;
        a.addEventListener('click', event => {
          event.preventDefault();
          const url = a.dataset.url;
          const loading = document.getElementById("loading");
          loading.style.display = "block";
        
          fetch(`/download?url=${url}`)
              .then(response => response.json())
              .then(data => {
                console.log(data);
                  if (data.success) {
                      window.location.href = '/play/';
                  } else {
                      document.getElementById("download_r").innerHTML = data.message;          
                  }
              })
              .catch(error => {
                  console.error(error);
              })
              .finally(() => {
                  loading.style.display = "none";
              });
        });

        author.textContent = video.author || "Unknown";
        authorImg.src = video.author_img || "https://via.placeholder.com/50x50.png?text=No+Image";
        authorImg.alt = "none";
        authorImg.width = "50";

        td1.appendChild(img);
        td2.appendChild(a);
        td3.appendChild(authorImg);
        td4.appendChild(author);
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tableBody.appendChild(tr);
      });
      table_title.style.display = "block";
      loading.style.display = "none";
    });
}


