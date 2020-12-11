function ConfModal(msg){
	var confModalId = '#confirmation-modal';

	this.onok = ()=> {};
	this.oncancel = ()=> {};

	$('body').append($(`
		<div class="modal fade" id="confirmation-modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-body">
						${msg}
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-dismiss="modal" id="cancel-opt">cancel</button>
						<button type="button" class="btn btn-danger" id="yes-opt">delete</button>
					</div>
				</div>
			</div>
		</div>
	`));
	$(confModalId).modal('show');
	$(confModalId).on('hidden.bs.modal', function (event) {
		$(confModalId).remove();
	});
	$('#yes-opt').on('click', (e) => {this.onok(); $(confModalId).modal('hide');});
	$('#cancel-opt').on('click', (e) => {this.oncancel()});
};