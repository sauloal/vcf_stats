        //var data = google.visualization.arrayToDataTable([
        //  ['Month', 'Bolivia', 'Ecuador', 'Madagascar', 'Papua New Guinea', 'Rwanda', 'Average'],
        //  ['2004/05',  165,      938,         522,             998,           450,      614.6],
        //  ['2005/06',  135,      1120,        599,             1268,          288,      682],
        //  ['2006/07',  157,      1167,        587,             807,           397,      623],
        //  ['2007/08',  139,      1110,        615,             968,           215,      609.4],
        //  ['2008/09',  136,      691,         629,             1026,          366,      569.6]
        //]);

        //var options = {
        //  title : 'Monthly Coffee Production by Country',
        //  vAxis: {title: "Cups"},
        //  hAxis: {title: "Month"},
        //  seriesType: "bars",
        //  series: {5: {type: "line"}}
        //};



       //var data = google.visualization.arrayToDataTable([
       //   ['Mon', 20, 28, 38, 45],
       //   ['Tue', 31, 38, 55, 66],
       //   ['Wed', 50, 55, 77, 80],
       //   ['Thu', 77, 77, 66, 50],
       //   ['Fri', 68, 66, 22, 15]
       //   // Treat first row as data as well.
       // ], true);

var VAXIS_FONTSIZE   = 11;
var HAXIS_FONTSIZE   = 11;
var LEGEND_FONTSIZE  = 11;
var TOOLTIP_FONTSIZE = 11;


function fixStr( src ) {
  return src.replace(/\//g, "_")
            .replace(/\\\\/g,"_")
            .replace(/\./g,"_")
            .replace(/ /g,"_")
            .replace(/\)/g,"_")
            .replace(/\(/g,"_")
            .replace(/\:/g,"_")
            .replace(/\-/g,"_")
            .replace(/#/g,"_")
            .replace(/\\%%/g,"_")
            .replace(/_+/g,"_");
}

function createDiv( dn, el, className ) {
    var nel = fixStr( el        );
    var ncn = className.join(" "); //fixStr( className );

    var ndiv = document.createElement('div');
    ndiv.setAttribute( "id"   , nel        );
    ndiv.setAttribute( "class", ncn        );

    var src = document.getElementById( dn );
    //console.log("createDiv DN", dn, 'SRC', src, 'EL', nel, 'NDIV', ndiv);
    src.appendChild( ndiv );
    return nel;
}


function drawVisualization(datain, el, options, chartType, firstrowasdata) {
  //console.log("drawVisualization",datain, el, options, chartType, firstrowasdata);
  var data  = google.visualization.arrayToDataTable(datain, firstrowasdata);
  var chart = new chartType( document.getElementById(el) );
  chart.draw(data, options);
}




function printer( title, vAxis, hAxis, datain, dn, el, classes, charType, frad ) {
  var options = {
      title          :   title,
      vAxis          : { title: vAxis ,                   textStyle: {fontSize: VAXIS_FONTSIZE   } },
      hAxis          : { title: hAxis , showTextEvery: 1, textStyle: {fontSize: HAXIS_FONTSIZE   } },
      legend         : {                                  textStyle: {fontSize: LEGEND_FONTSIZE  } },
      tooltip        : {                                  textStyle: {fontSize: TOOLTIP_FONTSIZE } },
      backgroundColor: { fill: 'transparent' },
      legend         : 'none'
    };

  var nel = createDiv( dn, el, classes );

  drawVisualization(datain, nel, options, charType, false);
}




function printcount(  filename, dn, name, data, title, vAxis, hAxis, headers, classes ) {
  //console.log( "print count", filename, dn, name, data );

  var datain = [ headers ];

  for ( key in data ) {
     var count = data[key];
     datain.push([ key, count ]);
  }
  //console.log("data in", datain);

  var el      = dn + '_' + name;

  var charType = google.visualization.ColumnChart;

  printer(title, vAxis, hAxis, datain, dn, el, classes, charType, false);
};


function printsingle( filename, dn, name, data, title, vAxis, hAxis, headers, classes ) {
  //console.log( "print single", filename, dn, name, data );

  var datain = [ headers ];

  for ( key in data ) {
     var vals = data[key];
     //-stddev +stddev min max
     var avg    = vals.average;
     var stddev = vals.stddev;
     var minV   = vals.min;
     var maxV   = vals.max;
     var low    = avg - stddev;
     var high   = avg + stddev;
     datain.push([ key, minV, low, high, maxV ]);
  }
  //console.log("data in", datain);

  var el      = dn + '_' + name;

  var charType = google.visualization.CandlestickChart;

  printer(title, vAxis, hAxis, datain, dn, el, classes, charType, false);
};




function printdouble( filename, dn, name, data, title, vAxis, hAxis, headers, classes1, classes2 ) {
  //console.log( "print double", filename, dn, name, data );

  var grp      = createDiv( dn, dn + '_' + name, classes1 );
  var clh      = classes1;
  clh.push("lbl2");
  var header   = createDiv( grp, dn + '_' + name + '_header', clh );
  document.getElementById( header ).innerHTML = name;

  for ( dclass in data ) {
    var ddata  = data[dclass];
    var name2  = name  + '_'   + dclass;
    var title2 = title + ' - ' + dclass;
    var vAxis2 = vAxis + ' - ' + dclass;
    var hAxis2 = hAxis;
    var classes22 = classes2;
    classes22.push( fixStr(dclass)              );
    classes22.push( fixStr(name + ' ' + dclass) );

    printsingle( filename, dn, name2, ddata, title2, vAxis2, hAxis2, headers, classes22 )
  }
};






function hideAllFilenames(){
  var flds = document.getElementsByTagName('*');
  for ( var f in flds ) {
     if ( ( ' ' + flds[f].className + ' ').indexOf(" filename ") > 1 ) {
       flds[f].style.visibility = 'hidden';
     }
  }
}

function selchange() {
  var x = document.getElementById("selector").selectedIndex;
  var v = document.getElementsByTagName("option")[x].value;
  if ( v == "_NONE_" ) {
    //hideAllFilenames();
    deletedata();
  } else {
    //hideAllFilenames();

    //alert( v );
    deletedata();
    showdata( v );
  }
}

function deletedata() {
  var el = document.getElementById( 'display' );
  if ( el ) {
    el.parentNode.removeChild( el );
  }
}


var dst_div = 'chart_div';

function showdata( filename ) {
  var filedata = window.dataall[ filename ];
  var divname  = fixStr( filename );
  console.log(" ", divname, filedata);

  var displaydiv = createDiv( dst_div   , "display"          , [] );

  var ndivname   = createDiv(   displaydiv, divname            , [ "l0", "filename" ] );

  var header     = createDiv(   ndivname, divname + '_header', [ "l0", "filename", "lbl1" ] );
  document.getElementById( header ).innerHTML = filename;

  var countdata        = filedata.count;
  var distancedata     = filedata.dist;
  var formatdata       = filedata.format;
  var infodata         = filedata.info;
  var polymorphismdata = filedata.polytype;
  var qualitydata      = filedata.qual;

  //console.log( "  count"   , countdata        );
  //console.log( "  distance", distancedata     );
  //console.log( "  format"  , formatdata       );
  //console.log( "  info"    , infodata         );
  //console.log( "  poly"    , polymorphismdata );
  //console.log( "  qualy"   , qualitydata      );

  name = "Count";        fname=fixStr(name); printcount(  filename, ndivname, name, countdata       , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Count']                    , [ "l1", "count"                ] );
  name = "Distance";     fname=fixStr(name); printsingle( filename, ndivname, name, distancedata    , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ]                  );
  name = "Quality";      fname=fixStr(name); printsingle( filename, ndivname, name, qualitydata     , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ], [ 'l2', fname ] );
  name = "Format";       fname=fixStr(name); printdouble( filename, ndivname, name, formatdata      , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ], [ 'l2', fname ] );
  name = "Info";         fname=fixStr(name); printdouble( filename, ndivname, name, infodata        , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ], [ 'l2', fname ] );
  name = "Polymorphism"; fname=fixStr(name); printdouble( filename, ndivname, name, polymorphismdata, filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ], [ 'l2', fname ] );

  document.getElementById(ndivname).style.visibility = 'visible';
}

function onLoad() {
  var keys = Object.keys(window.dataall);
  if ( keys.length == 1 ) {
      console.log('single file', keys, keys[0]);
      showdata( keys[0] );

  } else {
      console.log('multiple files', keys);
      var sel = document.createElement('select');
      sel.setAttribute('id'      , 'selector'    );
      sel.setAttribute('onchange', 'selchange();');

      var lnkg = document.createElement('option');
      lnkg.setAttribute("value", '_NONE_');
      lnkg.innerHTML = 'Please select file';
      sel.appendChild( lnkg );

      document.getElementById( "header" ).appendChild( sel );

      for ( var filepos in keys ) {
        var filename = keys[filepos];
        console.log(filename);

        var lnk = document.createElement('option');
        lnk.setAttribute("value", filename);
        lnk.innerHTML = filename;
        document.getElementById( "selector" ).appendChild( lnk );
      }
  }
}