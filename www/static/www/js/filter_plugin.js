function setPosArtList()
{
  var top=$("#filter").offset().top+$("#filter").height();
  $("#articleList").css("margin-top",top);
}

function getQueryString()
{
  var r=window.location.pathname.match(/blogs\/([0-9]+)\/([0-9]+)/);
  return parseInt(r[1]);
}

$("#filter").on("click","a",function()
		{
		  $("#filter a").removeClass("filterChoose");
		  $(this).addClass("filterChoose");
		  $(this).removeClass("filterUnChoose");
		})

$(document).ready(function()
		{
		  $("#filter a").addClass("filterUnChoose");
		  $("#filter a").eq(parseInt(getQueryString())).click();
		  setPosArtList();
		})
