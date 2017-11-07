//$(document).ready(function() {
function setDatePicker() {
  $('input.md_datepicker').datepicker({
    format: "yyyy-mm-dd",
    maxViewMode: 3,
    todayBtn: "linked",
    clearBtn: true,
    language: "cs",
    daysOfWeekHighlighted: "0,6",
    todayHighlight: true
  });
};
