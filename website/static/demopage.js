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
      document.getElementById('endDate').value = date;
      document.getElementById('firstRow').style.display = 'none';
      document.getElementById('secondRow').style.display = 'block';

      var outputDiv = document.getElementById('autosOutput');
      outputDiv.innerHTML = '';

      for (var i = 0; i < aantalAutos; i++) {
        var autoOpties = document.createElement('div');
        autoOpties.classList.add('autoOpties');
        autoOpties.classList.add('row');
        autoOpties.style.padding='0vh';
        

        var optiesText = document.createElement('div');
        optiesText.classList.add('col');
        autoOpties.appendChild(optiesText);

        var text = document.createElement('h2');
        optiesText.appendChild(text);
        text.textContent = 'Car ' + (i + 1) + ':';
        text.style.fontSize = '3vmin';
        text.style.position = 'absolute';
        text.style.top = '50%';
        text.style.transform = 'translate(0vmin,calc(-50%))';
        optiesText.style.setProperty('padding-left', '2vmin');
        // optiesText.style.width = '14.28vmin';

        var optiesType = document.createElement('div');
        autoOpties.appendChild(optiesType);
        optiesType.classList.add('col');
        // optiesType.style.setProperty('padding-left', '0vmin');
        // optiesType.style.setProperty('padding-right', '0vmin');
        optiesType.style.padding = '1vmin'
        // optiesType.style.width = '14.28vmin';

        var Type = document.createElement('select');
        optiesType.appendChild(Type);
        Type.classList.add('form-select');
        Type.classList.add('soort-auto');
        // Type.style.float= 'left';
        Type.style.fontSize = '2vmin';
        Type.style.width = '13vmin';

        var hybrydeOptie = document.createElement('option');
        Type.appendChild(hybrydeOptie);
        hybrydeOptieText = document.createElement('p');
        hybrydeOptieText.innerHTML = 'Hybrid Car';
        hybrydeOptie.appendChild(hybrydeOptieText);
        hybrydeOptie.value = 1;

        var elektrischeOptie = document.createElement('option');
        Type.appendChild(elektrischeOptie);
        elektrischeOptieText = document.createElement('p');
        elektrischeOptieText.innerHTML = 'Electrical Car';
        elektrischeOptie.appendChild(elektrischeOptieText);
        elektrischeOptie.value = 2;

        var huidigPercentageHolder = document.createElement('div');
        huidigPercentageHolder.classList.add('row');
        huidigPercentageHolder.style.display = 'grid'; 

        var huidigPercentage = document.createElement('input');
        huidigPercentage.id = "huidigPercentage" + (i + 1);
        huidigPercentage.setAttribute('auto', (i + 1));
        huidigPercentage.type = 'range';
        huidigPercentage.min = 0;
        huidigPercentage.max = 100;
        huidigPercentage.value = 50;
        huidigPercentage.step = 2;
        // huidigPercentage.classList.add('col');
        huidigPercentage.classList.add('inputPercentage');
        // huidigPercentage.style.float= 'left';
        huidigPercentage.style.display = 'grid';

        var optiesHuidigPercentage = document.createElement('div');
        optiesHuidigPercentage.classList.add('col');
        optiesHuidigPercentage.style.display = 'grid';
        // optiesHuidigPercentage.style.setProperty('padding-left', '0vmin');
        // optiesHuidigPercentage.style.setProperty('padding-right', '0vmin');
        optiesHuidigPercentage.style.padding = '1vmin';

        var sliderValue = document.createElement('div');
        // sliderValue.classList.add('col');
        sliderValue.id = 'huidigPercentageAankomst' + (i + 1);
        sliderValue.name = 'huidigPercentageAankomst' + (i + 1);
        sliderValue.textContent=huidigPercentage.value;
        sliderValue.style.fontSize = '2.8vmin';
        // sliderValue.style.float= 'left';
        sliderValue.style.display='grid';

        sliderInput = document.createElement('input');
        sliderInput.id = 'percentageAankomst' + (i + 1);
        sliderInput.name = 'percentageAankomst' + (i + 1);
        sliderInput.type = 'text';
        sliderInput.style.display = 'none';
        sliderInput.value = huidigPercentage.value;
        
        autoOpties.appendChild(optiesHuidigPercentage);
        optiesHuidigPercentage.appendChild(huidigPercentageHolder);
        huidigPercentageHolder.appendChild(sliderValue);
        huidigPercentageHolder.appendChild(huidigPercentage);
        huidigPercentageHolder.appendChild(sliderInput);

        var gewenstPercentage = document.createElement('input');
        gewenstPercentage.id = "gewenstPercentage" + (i + 1);
        gewenstPercentage.setAttribute('auto', (i + 1));
        gewenstPercentage.type = 'range';
        gewenstPercentage.min = 50;
        gewenstPercentage.max = 100;
        gewenstPercentage.value = 50;
        gewenstPercentage.step = 2;
        // gewenstPercentage.classList.add('col');
        gewenstPercentage.classList.add('outputPercentage');
        // gewenstPercentage.style.float= 'left';
        gewenstPercentage.style.display='grid';

        var optiesGewenstPercentage = document.createElement('div');
        optiesGewenstPercentage.classList.add('col');
        // optiesGewenstPercentage.style.setProperty('padding-left', '0vmin');
        // optiesGewenstPercentage.style.setProperty('padding-right', '0vmin');
        optiesGewenstPercentage.style.padding = '1vmin';
        // optiesGewenstPercentage.style.width = '14.28vmin';

        var sliderValue2 = document.createElement('div');
        // sliderValue2.classList.add('col');
        sliderValue2.id = 'huidigPercentageGewenst' + (i + 1);
        sliderValue2.name = 'huidigPercentageGewenst' + (i + 1);
        sliderValue2.textContent=gewenstPercentage.value;
        sliderValue2.classList.add('sliderValue');
        sliderValue.classList.add('sliderValue');
        sliderValue2.style.fontSize = '2.8vmin';
        // sliderValue2.style.float= 'left';

        sliderInput2 = document.createElement('input');
        sliderInput2.id = 'percentageGewenst' + (i + 1);
        sliderInput2.name = 'percentageGewenst' + (i + 1);
        sliderInput2.type = 'text';
        sliderInput2.style.display = 'none';
        sliderInput2.value = gewenstPercentage.value;
        
        var optiesGewenstPercentageHolder = document.createElement('div');
        optiesGewenstPercentageHolder.classList.add('row');
        optiesGewenstPercentageHolder.style.display = 'grid';

        autoOpties.appendChild(optiesGewenstPercentage);
        optiesGewenstPercentage.appendChild(optiesGewenstPercentageHolder);
        optiesGewenstPercentageHolder.appendChild(sliderValue2);
        optiesGewenstPercentageHolder.appendChild(gewenstPercentage);
        optiesGewenstPercentageHolder.appendChild(sliderInput2);

        var aankomstVertrek = document.createElement('div');
        // aankomstVertrek.style.width = '14.28vmin';
        aankomstVertrek.classList.add('col');
        var aankomstVertrekHolder = document.createElement('div');
        // aankomstVertrekHolder.style.float= 'left';
        aankomstVertrekHolder.style.display='grid';
        aankomstVertrekHolder.classList.add('row');
        aankomstVertrekHolder.classList.add('aankomstVertrekHolder');
        var aankomstHolder = document.createElement('div');
        aankomstHolder.style.display='grid';
        aankomstVertrekHolder.style.width = 'fit-content';
        // aankomstHolder.classList.add('row');
        var vertrekHolder = document.createElement('div');
        // vertrekHolder.classList.add('row');
        vertrekHolder.style.display='grid';
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
        aankomst.classList.add('aankomst');
        aankomst.setAttribute('auto', (i + 1));
        aankomst.style.width = '18vmin';
        aankomst.value='08:00';
        aankomst.style.fontSize = '2.8vmin';

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
        vertrek.style.width = '18vmin';
        vertrek.value = '17:00';
        vertrek.style.fontSize = '2.8vmin';

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
        slider.nextElementSibling.value = slider.value;
        if (parseInt(document.getElementById('gewenstPercentage' + (slider.getAttribute('auto'))).value) < parseInt(slider.value)){
          document.getElementById('gewenstPercentage' + (slider.getAttribute('auto'))).value = slider.value;
          document.getElementById('huidigPercentageGewenst' + (slider.getAttribute('auto'))).textContent = slider.value;
          document.getElementById('percentageGewenst' + (slider.getAttribute('auto'))).value = slider.value;
        }else{}
        document.getElementById('gewenstPercentage' + (slider.getAttribute('auto'))).min = slider.value;
      });
      });
      
      const sliders2 = document.querySelectorAll('.outputPercentage');
      sliders2.forEach(slider2 => {
        slider2.addEventListener('input', function outputdynamic() {
        slider2.previousElementSibling.textContent = slider2.value;
        slider2.nextElementSibling.value = slider2.value;
      });
      });

      const aankomstUren = document.querySelectorAll('.aankomst');
      aankomstUren.forEach(aankomst => {
        aankomst.addEventListener('input', function aankomstdynamic() {
        document.getElementById('vertrekUur' + aankomst.getAttribute('auto')).min = aankomst.value;
      });
      });
    }
  }

  function dismiss(){
    document.getElementById('alertId').style.display = 'none';
  }

  function submitForm() {
    document.getElementById("calcData").submit();  // uncomment deze regel als je het formulier wilt indienen
  }



