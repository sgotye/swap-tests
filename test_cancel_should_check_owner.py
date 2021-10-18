from pytezos import ContractInterface, MichelsonRuntimeError
import pytest
  

SWAP_FN = 'build/swap.tz'
sender = 'tz1ape24WMR4QmThsUujAYcB2xTHLr23kLhA'

list_params = {
    'ask_price': 1_000_000,
    'token_id': 5
}

def assert_list_result():
    contract = ContractInterface.from_file(SWAP_FN)

    init_storage = {
        'swaps': {},
        'token_address': 'KT1A2smYFA2zkGcji868B435oMAL1NCKRgMo',
        'metadata': {}
    }

    result = contract.list(list_params).interpret(storage=init_storage, sender=sender)
    result_swaps = result.storage['swaps']

    assert result_swaps.get(5) is not None
    assert result_swaps[5]['owner'] == sender
    return contract, result

def test_should_check_owner_when_cancel_called():
    contract, result = assert_list_result()
    new_sender = 'tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'
    with pytest.raises(MichelsonRuntimeError) as err:
        result = contract.cancel(5).interpret(storage=result.storage, sender=new_sender)
    assert 'Only the owner can cancel the swap' in str(err)

def test_should_check_token_id_when_list_called():
    contract, result = assert_list_result()
    new_sender = 'tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'

    # When there is no check if the token id exists, the token owner will be rewritten.
    # It will become new_sender and the original one will lose the token.
    with pytest.raises(MichelsonRuntimeError) as err:
        result = contract.list(list_params).interpret(storage=result.storage, sender=new_sender)
    assert 'The swap already exists' in str(err)

