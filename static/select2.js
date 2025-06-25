$(document).ready(function() {
    $('#position-filter').select2({
        placeholder: 'Select position',
        allowClear: true
    });

    $('#class-filter').select2({
        placeholder: 'Select graduating class',
        allowClear: true
    });

    $('#team-filter').select2({
        placeholder: 'Select team',
        allowClear: true
    });

    $('#weight-filter').select2({
        placeholder: 'Select weight range',
        allowClear: true
    });

    $('#height-filter').select2({
        placeholder: 'Select height range',
        allowClear: true
    });
    
    $('#region-filter').select2({
        placeholder: 'Select state or country',
        allowClear: true
    });

});


function applyFilters() {
    const selectedPositions = $('#position-filter').val();
    const selectedClasses = $('#class-filter').val();
    const selectedTeams = $('#team-filter').val();   
    const selectedRegions = $('#region-filter').val();
    const selectedWeights = $('#weight-filter').val();
    const selectedHeights = $('#height-filter').val();

    $('#player-table tbody tr').each(function() {
        const row =$(this);
        const position = row.data('position')
        const gradClass = row.data('class')
        const team = row.data('team')
        const region = row.data('region')
        const weight = row.data('weight')
        const height = row.data('height');
        
        const matchHeight = !selectedHeights || selectedHeights.length === 0 || selectedHeights.includes(height);
        const matchRegion = !selectedRegions || selectedRegions.length === 0 || selectedRegions.includes(region);
        const matchPosition = !selectedPositions || selectedPositions.length === 0 || selectedPositions.includes(position);
        const matchClass = !selectedClasses || selectedClasses.length === 0 || selectedClasses.includes(gradClass);
        const matchTeam = !selectedTeams || selectedTeams.length === 0 || selectedTeams.includes(team);
        const matchWeight = !selectedWeights || selectedWeights.length === 0 || selectedWeights.includes(weight);


        if (matchRegion && matchPosition && matchClass && matchTeam && matchWeight && matchHeight) {
            row.show();
        } else {
            row.hide();
        }
    });
}
