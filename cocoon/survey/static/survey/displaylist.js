/**
 * Created by srayment on 3/1/18.
 */

var isVisible = false;
function toggleList() {

    if (!isVisible) {
      $(".export-modal").show();
      isVisible = true
    } else {
      $(".export-modal").hide();
      isVisible = false;
    }
}