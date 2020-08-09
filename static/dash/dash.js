let appUrl = "https://clubs-app-john.herokuapp.com/";

$(function () {
  $(".nav-link").click(function () {
    $(".active").removeClass("active");
    $(this).addClass("active");
    if ($(this).attr("val") == "form") {
      $("#form").show();
      $("#clubs").hide();
    }
    if ($(this).attr("val") == "clubs") {
      $("#form").hide();
      $("#clubs").show();
    }
  });
  $("#search").on("input", function () {
    let value = $(this).val();
    if (!value) {
      $("tbody>tr").show();
      return;
    }
    let regex = new RegExp("^" + value, "i");
    $("tbody>tr").each(function () {
      if (!$(this).attr("class").match(regex)) {
        $(this).hide();
      }
    });
  });
  $(".edit-btn").click(function () {
    let id = $(this).attr("club_id");
    let clubName = $(this).attr("clubName");
    let category = $(this).attr("category");
    let public = $(this).attr("public");
    $("#m_clubName").val(clubName);
    $("#m_categories").val(category).change();
    $("#m_public").val(public).change();
    $(".update-btn").attr("club_id", id);
    $(".delete-btn").attr("club_id", id);
  });
  $(".update-btn").click(function () {
    let id = $(this).attr("club_id");
    updateClub(
      id,
      $("#m_clubName").val(),
      $("#m_categories").val(),
      $("#m_public").val()
    );
    $("#updateModal").modal("hide");
  });
  $(".delete-btn").click(function () {
    let id = $(this).attr("club_id");
    deleteClub(id);
    $("#updateModal").modal("hide");
  });
});

function addClub() {
  let xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState == 4) {
      alert(this.response);
    }
  };
  xhr.open("POST", appUrl + "addClub", true);
  let clubName = $("#clubName").val();
  let category = $("#categories").val();
  let public = $("#public").val();
  let body = { clubName, category, public };
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify(body));
}

function updateClub(club_id, clubName, category, public) {
  let xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState == 4) {
      alert(this.response);
    }
  };
  xhr.open("POST", appUrl + "updateClub", true);
  let body = { club_id, clubName, category, public };
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify(body));
}

function deleteClub(club_id) {
  let xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState == 4) {
      alert(this.response);
    }
  };
  xhr.open("DELETE", appUrl + "deleteClub", true);
  xhr.setRequestHeader("club_id", `${club_id}`);
  xhr.send();
}
