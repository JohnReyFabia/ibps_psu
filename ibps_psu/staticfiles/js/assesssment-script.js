// var currentTab = 0; // Current tab is set to be the first tab (0)
// showTab(currentTab); // Display the current tab

// function showTab(n) {
//   // This function will display the specified tab of the form ...
//   var x = document.getElementsByClassName("poll");
//   x[n].style.display = "flex";
//   // ... and fix the Previous/Next buttons:
//   if (n == 0) {
//     document.getElementById("prevBtn").style.display = "none";
//   } else {
//     document.getElementById("prevBtn").style.display = "inline";
//   }
//   if (n == (x.length - 1)) {
//     document.getElementById("nextBtn").innerHTML = "Submit";
//   } else {
//     document.getElementById("nextBtn").innerHTML = "Next";
//   }
//   // ... and run a function that displays the correct step indicator:
//   fixStepIndicator(n)
// }

// function nextPrev(n) {
//   // This function will figure out which tab to display
//   var x = document.getElementsByClassName("poll");
//   // Exit the function if any field in the current tab is invalid:
//   if (n == 1 && !validateForm()) return false;
//   // Hide the current tab:
//   x[currentTab].style.display = "none";
//   // Increase or decrease the current tab by 1:
//   currentTab = currentTab + n;
//   // if you have reached the end of the form... :
//   if (currentTab >= x.length) {
//     //...the form gets submitted:
//     document.getElementById("regForm").submit();
//     return false;
//   }
//   // Otherwise, display the correct tab:
//   showTab(currentTab);
// }

// function validateForm() {
//   // This function deals with validation of the form fields
//   var x, y, i, valid = true;
//   x = document.getElementsByClassName("tab");
//   y = x[currentTab].getElementsByTagName("input");
//   // A loop that checks every input field in the current tab:
//   for (i = 0; i < y.length; i++) {
//     // If a field is empty...
//     if (y[i].value == "") {
//       // add an "invalid" class to the field:
//       y[i].className += " invalid";
//       // and set the current valid status to false:
//       valid = false;
//     }
//   }
//   // If the valid status is true, mark the step as finished and valid:
//   if (valid) {
//     document.getElementsByClassName("step")[currentTab].className += " finish";
//   }
//   return valid; // return the valid status
// }

// function fixStepIndicator(n) {
//   // This function removes the "active" class of all steps...
//   var i, x = document.getElementsByClassName("step");
//   for (i = 0; i < x.length; i++) {
//     x[i].className = x[i].className.replace(" active", "");
//   }
//   //... and adds the "active" class to the current step:
//   x[n].className += " active";
// }





// document.addEventListener('DOMContentLoaded', function () {
//   var form = document.querySelector('form');

//   form.addEventListener('change', function (event) {
//     var target = event.target;

//     if (target.type === 'radio' && target.name.startsWith('question')) {
//       var options = document.querySelectorAll('.option');
//       options.forEach(function (option) {
//         option.classList.remove('selected');
//       });

//       var selectedLi = target.closest('li');
//       selectedLi.classList.add('selected');
//     }
//   });
// });

document.addEventListener('DOMContentLoaded', function () {
  var form = document.querySelector('form');

  // Add event listeners to all radio buttons
  form.querySelectorAll('input[type="radio"]').forEach(function (radio) {
    radio.addEventListener('change', function () {
      updateSelectedClass(radio.name);
    });
  });
});

function prevStep(currentStep) {
  var currentStepElement = document.getElementById('step' + currentStep);
  currentStepElement.classList.remove('visible');
  currentStepElement.classList.add('hidden');

  var prevStep = currentStep - 1;
  var prevStepElement = document.getElementById('step' + prevStep);
  prevStepElement.classList.remove('hidden');
  prevStepElement.classList.add('visible');

  updateSelectedClass();  // Update selected class when navigating back
}

function nextStep(nextStep) {
  var currentStepElement = document.getElementById('step' + (nextStep - 1));
  var selectedOption = currentStepElement.querySelector('input[name^="question"]:checked');

  if (!selectedOption) {
    alert('Please select an option before proceeding.');
    return;
  }

  updateSelectedClass();  // Update selected class before navigating to the next step

  currentStepElement.classList.remove('visible');
  currentStepElement.classList.add('hidden');

  var nextStepElement = document.getElementById('step' + nextStep);
  nextStepElement.classList.remove('hidden');
  nextStepElement.classList.add('visible');
}

function updateSelectedClass(questionName) {
  var form = document.querySelector('form');
  var options = form.querySelectorAll('input[name="' + questionName + '"]');

  options.forEach(function (option) {
    var selectedLi = option.closest('li');
    if (option.checked) {
      selectedLi.classList.add('selected');
    } else {
      selectedLi.classList.remove('selected');
    }
  });
}








// // Add this script after the HTML content
// document.addEventListener('DOMContentLoaded', function () {
//   var questions = document.querySelectorAll('.options-list');

//   questions.forEach(function (question) {
//     var optionsList = question.querySelectorAll('input[type="radio"]');

//     optionsList.forEach(function (radio) {
//       radio.addEventListener('change', function () {
//         // Remove 'selected' class only from options within the current question
//         question.querySelectorAll('.option').forEach(function (option) {
//           option.classList.remove('selected');
//         });

//         // Add 'selected' class to the parent li if the radio button is checked
//         if (radio.checked) {
//           radio.closest('li.option').classList.add('selected');
//         }
//       });
//     });
//   });
// });

