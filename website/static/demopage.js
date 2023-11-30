  document.getElementById("typeOfCalculation").onchange = changeListener;
  
  function changeListener(){
  var value = this.value
    
    if (value == "4"){
        document.getElementById('endDateCol').style.display = 'none';
        document.getElementById('endDate').value = document.getElementById('startDate').value;
        document.getElementById('aantalAutosRow').style.display = 'block';
        document.getElementById('full-sim-button').style.display = 'block';
        document.getElementById('other-button').style.display = 'none';
    }else{
        document.getElementById('endDateCol').style.display = 'block';
        document.getElementById('aantalAutosRow').style.display = 'none';
        document.getElementById('full-sim-button').style.display = 'none';
        document.getElementById('other-button').style.display = 'block';
    }
    
  }

  function proceedCalc(){
    var date = document.getElementById('startDate').value;
    var aantalAutos = document.getElementById('aantalAutos').value;
    console.log(document.getElementById('aantalAutos').value);
    if (date == '' || aantalAutos== ''){
      document.getElementById('alertId').style.display = 'block';
    }else{
      document.getElementById('firstRow').style.display = 'none';
      document.getElementById('secondRow').style.display = 'block';

      var outputDiv = document.getElementById('autosOutput');
      outputDiv.innerHTML = '';

      for (var i = 0; i < aantalAutos; i++) {
        var autoOpties = document.createElement('div');
        autoOpties.classList.add('autoOpties');
        autoOpties.classList.add('row');

        var optiesText = document.createElement('div');
        optiesText.classList.add('col');
        autoOpties.appendChild(optiesText);

        var text = document.createElement('h2');
        optiesText.appendChild(text);
        text.textContent = 'Wagen ' + (i + 1) + ':';

        var optiesType = document.createElement('div');
        autoOpties.appendChild(optiesType);
        optiesType.classList.add('col');

        var Type = document.createElement('select');
        optiesType.appendChild(Type);
        Type.classList.add('form-select');

        var hybrydeOptie = document.createElement('option');
        Type.appendChild(hybrydeOptie);
        hybrydeOptie.textContent = 'Hybride Wagen';
        hybrydeOptie.value = 1;

        var elektrischeOptie = document.createElement('option');
        Type.appendChild(elektrischeOptie);
        elektrischeOptie.textContent = 'Elektrische Wagen';
        elektrischeOptie.value = 2;

        var huidigPercentage = document.createElement('input');
        huidigPercentage.id = "huidigPercentage" + (i + 1);
        huidigPercentage.type = 'range';
        huidigPercentage.min = 0;
        huidigPercentage.max = 100;
        huidigPercentage.value = 50;
        huidigPercentage.step = 2;
        huidigPercentage.classList.add('col');
        huidigPercentage.classList.add('inputPercentage');

        var optiesHuidigPercentage = document.createElement('div');
        optiesHuidigPercentage.classList.add('col');

        var sliderValue = document.createElement('div');
        sliderValue.classList.add('col');
        sliderValue.id = 'huidigPercentageAankomst' + (i + 1);
        sliderValue.textContent=huidigPercentage.value;
        
        autoOpties.appendChild(optiesHuidigPercentage);
        optiesHuidigPercentage.appendChild(sliderValue);
        optiesHuidigPercentage.appendChild(huidigPercentage);

        var gewenstPercentage = document.createElement('input');
        gewenstPercentage.id = "gewenstPercentage" + (i + 1);
        gewenstPercentage.type = 'range';
        gewenstPercentage.min = 0;
        gewenstPercentage.max = 100;
        gewenstPercentage.value = 50;
        gewenstPercentage.step = 2;
        gewenstPercentage.classList.add('col');
        gewenstPercentage.classList.add('outputPercentage');

        var optiesGewenstPercentage = document.createElement('div');
        optiesGewenstPercentage.classList.add('col');

        var sliderValue2 = document.createElement('div');
        sliderValue2.classList.add('col');
        sliderValue2.id = 'huidigPercentageGewenst' + (i + 1);
        sliderValue2.textContent=gewenstPercentage.value;
        
        autoOpties.appendChild(optiesGewenstPercentage);
        optiesGewenstPercentage.appendChild(sliderValue2);
        optiesGewenstPercentage.appendChild(gewenstPercentage);

        var aankomstVertrek = document.createElement('div');
        aankomstVertrek.classList.add('col');
        var aankomstVertrekHolder = document.createElement('div');
        aankomstVertrekHolder.classList.add('row');
        var aankomstHolder = document.createElement('div');
        aankomstHolder.classList.add('col');
        var vertrekHolder = document.createElement('div');
        vertrekHolder.classList.add('col');
        var aankomst = document.createElement('input');
        var vertrek = document.createElement('input');
        aankomstVertrek.appendChild(aankomstVertrekHolder);

        aankomst.type='text';
        aankomst.id = 'aankomstUur' + (i + 1);
        aankomst.name= 'aankomstUur' + (i + 1);
        aankomst.autocomplete='off';
        aankomst.min='06:00';
        aankomst.max='22:00';
        aankomst.step = '900';

        aankomstVertrekHolder.appendChild(aankomstHolder);
        aankomstHolder.appendChild(aankomst);
        
        outputDiv.appendChild(autoOpties);

        vertrek.type='text';
        vertrek.id = 'vertrekUur' + (i + 1);
        vertrek.name= 'vertrekUur' + (i + 1);
        vertrek.autocomplete='off';
        vertrek.min='07:00';
        vertrek.max='22:15';
        vertrek.step = '900';

        aankomstVertrekHolder.appendChild(vertrekHolder);
        vertrekHolder.appendChild(vertrek);
        autoOpties.appendChild(aankomstVertrek);

        jQuery('#aankomstUur' + (i + 1)).timepicker({
          format: 'HH:mm',
        });
        jQuery('#vertrekUur' + (i + 1)).timepicker({
          format: 'HH:mm',
        });
    }
      const sliders = document.querySelectorAll('.inputPercentage');
      sliders.forEach(slider => {
        slider.addEventListener('input', function inputdynamic() {
        slider.previousElementSibling.textContent = slider.value;
      });
      });
      
      const sliders2 = document.querySelectorAll('.outputPercentage');
      sliders2.forEach(slider2 => {
        slider2.addEventListener('input', function outputdynamic() {
        slider2.previousElementSibling.textContent = slider2.value;
      });
      });
    }
  }

  function dismiss(){
    document.getElementById('alertId').style.display = 'none';
  }



