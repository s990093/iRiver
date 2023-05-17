export function error(title, body) {
    $("#errorModal").modal("show");
    $("#errorModal").find(".modal-title").html(title);
    $("#errorModal").find(".modal-body").html(body);
}