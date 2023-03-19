function verificaHorario(varData, varHoraInicio, varHoraTermino,tabelaCargaHoraria, varTecnico){

    const linhas = tabelaCargaHoraria.rows;
    for (let i = 0; i < linhas.length; i++) {
        const celulas = linhas[i].cells;
        let data = celulas[0].textContent.trim();
        let horaInicio = celulas[1].textContent.trim();
        let horaTermino = celulas[2].textContent.trim();
        let tecnico = celulas[4].textContent.trim();
        
        if(varData==data & tecnico == varTecnico){
            if (horariosSeSobrepoe(horaInicio, horaTermino, varHoraInicio, varHoraTermino)){
                return true;
            }
        }

        
    }
    return false;
}



function formatarData(data){
    const partes = data.split("-"); // Divide a string em partes separadas por "-"
    const novaData = partes[2] + "/" + partes[1] + "/" + partes[0]; // Reorganiza as partes em nova string com a ordem desejada
    return novaData; 
}

function formatarHora(input){
    let [hora, min] = input.split(":"); 
    hora = hora.padStart(2, "0");  // adiciona zero à esquerda, se necessário
    return `${hora}:${min}`;  
}

function subtrairHorarios(horario1, horario2) {
    var partes1 = horario1.split(":");
    var partes2 = horario2.split(":");
    var data1 = new Date(0, 0, 0, partes1[0], partes1[1]);
    var data2 = new Date(0, 0, 0, partes2[0], partes2[1]);
    var diferenca = data2.getTime() - data1.getTime();
    var horas = Math.floor(diferenca / (1000 * 60 * 60));
    diferenca -= horas * (1000 * 60 * 60);
    var minutos = Math.floor(diferenca / (1000 * 60));
    if (minutos < 10) {
      minutos = "0" + minutos;
    }
    return horas + ":" + minutos;
}

function horariosSeSobrepoe(inicio1, fim1, inicio2, fim2) {
    // Converter horários em minutos a partir da meia-noite
    var inicioMinutos1 = horarioParaMinutos(inicio1);
    var fimMinutos1 = horarioParaMinutos(fim1);
    var inicioMinutos2 = horarioParaMinutos(inicio2);
    var fimMinutos2 = horarioParaMinutos(fim2);
  
    // Verificar se horário de início do primeiro intervalo ocorre durante o segundo intervalo
    if (inicioMinutos1 >= inicioMinutos2 && inicioMinutos1 < fimMinutos2) {
      return true;
    }
  
    // Verificar se horário de término do primeiro intervalo ocorre durante o segundo intervalo
    if (fimMinutos1 > inicioMinutos2 && fimMinutos1 <= fimMinutos2) {
      return true;
    }
  
    // Verificar se o primeiro intervalo abrange completamente o segundo intervalo
    if (inicioMinutos1 <= inicioMinutos2 && fimMinutos1 >= fimMinutos2) {
      return true;
    }
  
    // Se nenhum dos casos acima for verdadeiro, os intervalos não se sobrepõem
    return false;
}
  
function horarioParaMinutos(horario) {
    var partes = horario.split(':');
    return parseInt(partes[0]) * 60 + parseInt(partes[1]);
}