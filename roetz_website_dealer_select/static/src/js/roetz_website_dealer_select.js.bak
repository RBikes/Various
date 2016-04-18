
/**
 * Geocode an address via Google API
 *
 * @param {*} address
 * @returns {*}
 */
var geocodeAddress = function (address) {
    var dfd = jQuery.Deferred();
    var url = 'https://maps.googleapis.com/maps/api/geocode/json';

    // Utililty method
    function objToString (obj) {
        var str = [];
        for (var p in obj) {
            if (obj.hasOwnProperty(p)) {
                str.push(obj[p]);
            }
        }
        return str.join(', ');
    }

    // Object to string that google likes; Street X, City, Zip, Country
    address = objToString(address);

    $.getJSON(url, {'address': address}, function (data) {
        if (data.status == 'OK' && data.results.length) {
            data = data.results[0];

            $('.js_nearby_dealer_table').trigger( "Geocode_FormattedAddressResult", [ data.formatted_address ]  );

            dfd.resolve(data.geometry.location);
        } else {
            $('.js_nearby_dealer_table').trigger( "Geocode_FormattedAddressResult", [ 'Roetz-Bikes Head Quarter' ]  );
            dfd.resolve({'lat': 52.350616, 'lng': 4.832619}); // roetz ottho
           // dfd.reject('Geocoding of address failed');
        }
    });

    return dfd.promise();
};

/**
 *
 * @param distance
 * @param lat
 * @param lng
 * @returns {*}
 */
var queryNearbyDealers = function(location) {
    var dfd = jQuery.Deferred();
    var url = '/shop/nearby_dealers';

    openerp.jsonRpc(
        url, 'method_call' /* ignored method */,
        {'distance': 20, 'lat': location.lat, 'lng': location.lng})
        .then(function (data) {
            dfd.resolve(data);
        }).fail(function() {
            dfd.reject('Querying nearby dealers failed');
        });

    return dfd.promise();
}

var markers = {}, infoWindow, map;

var renderInitialized = false;
var selectedDealer;
var renderNearbyDealers = function(dealers) {

    if (!map) {
        var mapCanvas = document.getElementById('map-canvas');
        var mapOptions = {zoom: 14, mapTypeId: google.maps.MapTypeId.ROADMAP};

        map = new google.maps.Map(mapCanvas, mapOptions);
        infoWindow = new google.maps.InfoWindow({});
    }

    $('.js_nearby_dealer_table').find('table tbody tr').remove();

    var trTmpl = '<tr>';
    trTmpl += '<td><input type="radio" name="optionsRadios" value="{dealer_id}"></td>';
    trTmpl += '<td><strong>{name}</strong></td>';
    trTmpl += '<td>{street}</td>';
    trTmpl += '<td>{city}{country}</td>';
    trTmpl += '<td>~{distance}km</td>';
    trTmpl += '</tr>';

    $(dealers).each(function(i, dealer) {
        var tr = trTmpl.replace("{dealer_id}", dealer.id);
        tr = tr.replace("{name}", dealer.name ? dealer.name : '-');
        tr = tr.replace("{street}", dealer.street ? dealer.street : '-');
        tr = tr.replace("{zip}", dealer.zip ? dealer.zip : '-');
        tr = tr.replace("{city}", dealer.city ? dealer.city : '-');
        if ($('select[name=country_id] option:selected').val() != dealer.country_id) {
            tr = tr.replace("{country}", ', ' + $('select[name=country_id] option[value=' + dealer.country_id + ']').text());
        } else {
            tr = tr.replace("{country}", '');
        }
        tr = tr.replace("{distance}", (dealer.distance / 1000).toFixed(1));
        var $tr = $(tr).data('dealer', dealer);
        $('.js_nearby_dealer_table').find('table tbody').append($tr);
    });

    /**
     * Applies jquery plugin to allow table body scrolling on our table
     */
    if (!renderInitialized) {
        $('.js_nearby_dealer_table').find('table.table-scroll').scrollTableBody({rowsToDisplay: 5});

        renderInitialized = true;
    }

    // re-copy header columns widths to scrollable tbody td widths
    var $scrollableTable = $('.jqstb-scroll table');
    $('.jqstb-header-table thead tr th').each(function(i, el) {
        $scrollableTable.find('tbody tr:first td').eq(i).css('width', $(this).css('width'));
    });

    /**
     * Remove known markers from map
     **/
    for (var key in markers) {
        if (markers.hasOwnProperty(key)) {
            markers[key].setMap(null);
        }
    }

    /**
     * Create, store and place markers on map
     */
    $(dealers).each(function(i, dealer) {
        var marker;

        // create marker if it does not exist in our dictionary
        if (markers[dealer.id]) {
            marker = markers[dealer.id];
        } else {
            var dealerLatlng = new google.maps.LatLng(dealer.lat, dealer.lng);

            // Create marker
            marker = new google.maps.Marker({
                position: dealerLatlng,
                title: dealer.name,
                dealerInfo: dealer
            });

            // Add click event to marker
            google.maps.event.addListener(marker, 'click', function() {
                $('.js_nearby_dealer_table').trigger( "Dealer_SelectedDealer", [ this.dealerInfo ]  );
            });

            // Store in dictionary
            markers[dealer.id] = marker;
        }

        // add marker to map
        marker.setMap(map);
    });


    $('.js_nearby_dealer_table').find('table tbody tr').on('click', function() {
        selectedDealer = $(this).data('dealer');
        $('.js_nearby_dealer_table').trigger( "Dealer_SelectedDealer", [ selectedDealer ] );
    });

    /*
     * When we previously had a dealer selected we should find the newly rendered radio button (by dealer_id) and
     * re-select it.
     */
    if (selectedDealer) {
        if ($('.js_nearby_dealer_table').find('table tbody tr input:radio[value='+selectedDealer.id+']')) {
            $('.js_nearby_dealer_table').find('table tbody tr input:radio[value='+selectedDealer.id+']').prop('checked', true);
        } else {
            selectedDealer = $('.js_nearby_dealer_table').find('table tbody tr:first-child').data('dealer');
            $('.js_nearby_dealer_table').trigger( "Dealer_SelectedDealer", [ selectedDealer ] );
        }
    } else {
        selectedDealer = $('.js_nearby_dealer_table').find('table tbody tr:first-child').data('dealer');
        $('.js_nearby_dealer_table').trigger( "Dealer_SelectedDealer", [ selectedDealer ] );
    }

}

var reprocess = function() {
    if ($('select[name=shipping_id]').val() != "-0.5") {
        return false;
    }

    var address = {};
    address.street = $('input[name=street2]').val();
    address.city = $('input[name=city]').val();
    address.zip = $('input[name=zip]').val();
    address.country = $('select[name=country_id] option:selected').text();

    geocodeAddress(address)
        .then(queryNearbyDealers)
        .then(function(dealers) {
            renderNearbyDealers(dealers);
        })
        .fail(function(error) {
            renderNearbyDealers([]);
        });
};

$(document).ready(function () {
    $('.oe_website_sale').each(function () {
        var oe_website_sale = this;

        var $shippingDifferent = $("select[name='shipping_id']", oe_website_sale);
        var $snipping = $(".js_shipping", oe_website_sale);
        var $dealerTbl = $(".js_nearby_dealer_table", oe_website_sale);
        var $dealerMap = $(".js_nearby_dealer_map", oe_website_sale);

        // do this via a timer as website_sale.js allready has run and binded a change event
        setTimeout(function() {
            $shippingDifferent.unbind('change');
            $shippingDifferent.change(function (event) {
                var value = +$shippingDifferent.val();

                var data = $shippingDifferent.find("option:selected").data();
                var $inputs = $snipping.find("input");
                var $selects = $snipping.find("select");

                $snipping.toggle(value == -1);
                $dealerTbl.toggle(value == -0.5);
                $dealerMap.toggle(value == -0.5);

                $inputs.attr("readonly", value <= 0 ? null : "readonly").prop("readonly", value <= 0 ? null : "readonly");
                $selects.attr("disabled", value <= 0 ? null : "disabled").prop("disabled", value <= 0 ? null : "disabled");

                $inputs.each(function () {
                    $(this).val(data[$(this).attr("name")] || "");
                });
            });

            /**
             * Main magic
             *
             * Binds a 'debounced' handler to the appropriate ui inputs
             */
            $('input[name=street2], input[name=city], input[name=zip], select[name=country_id], select[name=shipping_id]', oe_website_sale)
                .bind('change keyup', $.debounce(reprocess, 300));

        }, 250);

        // upon submission of the form, we must set the select box to '-new address-'
        $shippingDifferent.closest('form').on('submit', function() {
            if ($('select[name=shipping_id]', oe_website_sale).val() == -0.5) {
                $('select[name=shipping_id] option[value="-1"]', oe_website_sale).prop('selected', true);

                var $inputs = $snipping.find("input");
                var $selects = $snipping.find("select");
                //$inputs.attr("readonly", value <= 0 ? null : "readonly").prop("readonly", value <= 0 ? null : "readonly");
                //$selects.attr("disabled", value <= 0 ? null : "disabled").prop("disabled", value <= 0 ? null : "disabled");

            }
        });

        // upon page load, check current value and hide/show appropiate element
        var value = +$shippingDifferent.val();
        $snipping.toggle(value == -1);
        $dealerTbl.toggle(value == -0.5);
        $dealerMap.toggle(value == -0.5);

    });

    /**
     * Bind a custom event handler, whenever google's geocoding formatted_address has been returned
     */
    $(".js_nearby_dealer_table").on( "Geocode_FormattedAddressResult", function( event, formatted_address ) {
        $("small.geo_formatted_address", $(this)).html(formatted_address ? formatted_address : '-');
    });

    /**
     * Bind a custom event handler, whenever user selects a dealer
     *
     * - enter dealer data in shipping form
     * - center google map on selected dealer and 'open' point
     */
    $(".js_nearby_dealer_table").on( "Dealer_SelectedDealer", function( event, dealer ) {
        if (!dealer) {
            return;
        }

        // select checkbox
        $(".js_nearby_dealer_table table").find('td input:radio[value='+dealer.id+']').prop('checked', true);

        $('input[name=shipping_name]').val(dealer.name ? dealer.name : '');
        $('input[name=shipping_phone]').val(dealer.phone ? dealer.phone : 'n/a');
        $('input[name=shipping_street]').val(dealer.street ? dealer.street : 'n/a');
        $('input[name=shipping_zip]').val(dealer.zip ? dealer.zip : 'n/a');
        $('input[name=shipping_city]').val(dealer.city ? dealer.city : 'n/a');
        $('select[name=shipping_country_id] option[value="'+dealer.country_id+'"]').prop('selected', true);

        map.panTo(new google.maps.LatLng(dealer.lat, dealer.lng));

        var country = $('select[name=country_id] option[value=' + dealer.country_id + ']').text();
        var contentString =
            '<div id="content">' +
                '<h5 id="firstHeading" class="firstHeading" style="min-width: 200px; margin-top: 2px; margin-bottom: 2px;">' +
                '<a href="'+((dealer.website) ? dealer.website : '#')+'">' + dealer.name + '</a></h5>'+
                '<div id="bodyContent">'+
                    '<address style="margin-bottom: 0;">' +
                        dealer.street + '<br>' +
                        dealer.zip + '&nbsp;&nbsp;' +
                        dealer.city + '<br>' +
                        country + '<br>' +
                        (dealer.phone ? '<a href="tel:' + dealer.phone + '">' + dealer.phone+'</a>' : '') +
                    '</address>' +
                '</div>'+
            '</div>';

        infoWindow.setContent(contentString);
        infoWindow.open(map, markers[dealer.id]);
    });


    // When choosing an delivery carrier, update the quotation and the acquirers
    var $carrier = $("#delivery_carrier");
    $carrier.find("input[name='delivery_type']").click(function (ev) {
        var carrier_id = $(ev.currentTarget).val();
        window.location.href = '/shop/checkout?carrier_id=' + carrier_id;
    });

});
