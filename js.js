setTimeout(function () {
  new DataTable('#modal_liste_lots', {
    dom: 'Blfrtip',
    paging: true,
    ordering: false,
    pageLength: 10,
    scrollX: true,
    lengthMenu: [[10, 25, 50]],
    language: {
      lengthMenu: "Afficher _MENU_ lignes par page",
      zeroRecords: "Aucun résultat trouvé",
      info: "Affichage de _START_ à _END_ sur _TOTAL_ lignes",
      infoEmpty: "Aucune ligne à afficher",
      infoFiltered: "(filtré de _MAX_ lignes au total)",
      search: "Recherche :",
      paginate: {
        first: "Premier",
        last: "Dernier",
        next: "Suivant",
        previous: "Précédent"
      }
    }
  });
}, 500);